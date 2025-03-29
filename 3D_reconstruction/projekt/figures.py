import open3d as o3d
import numpy as np
import hdbscan
import random
from sklearn import linear_model
import time


def fit_sphere(points):
    A = np.c_[2 * points[:, 0], 2 * points[:, 1], 2 * points[:, 2], np.ones(points.shape[0])]
    f = np.c_[points[:, 0] ** 2 + points[:, 1] ** 2 + points[:, 2] ** 2]
    C, _, _, _ = np.linalg.lstsq(A, f, rcond=None)
    center = C[0:3].flatten()
    radius = np.sqrt(C[3] + center.dot(center))
    return center, radius


def ransac_sphere(points, distance_threshold, num_iterations=1000):
    max_radius = 0.3
    best_inliers = []
    best_model = None

    for _ in range(num_iterations):
        sample_indices = np.random.choice(points.shape[0], 4, replace=False)
        sample_points = points[sample_indices]

        try:
            center, radius = fit_sphere(sample_points)

            if radius > max_radius:
                continue

            distances = np.linalg.norm(points - center, axis=1) - radius
            inliers = np.where(np.abs(distances) < distance_threshold)[0]

            if len(inliers) > len(best_inliers):
                best_inliers = inliers
                best_model = (center, radius)

        except np.linalg.LinAlgError:
            continue

    return best_model, best_inliers


def segment_plane_and_extract(current_cloud, distance_threshold=0.02, ransac_n=3, num_iterations=1000):
    try:
        plane_model_next, inliers_next = current_cloud.segment_plane(distance_threshold=distance_threshold,
                                                                     ransac_n=ransac_n,
                                                                     num_iterations=num_iterations)
        inlier_next_cloud = current_cloud.select_by_index(inliers_next)
        outlier_next_cloud = current_cloud.select_by_index(inliers_next, invert=True)
        return plane_model_next, inlier_next_cloud, outlier_next_cloud
    except:
        return None, None, None


def check_plane_orientation(plane_model, existing_plane, threshold=0.05):
    normal_dot_product = np.dot(plane_model[:3], existing_plane[:3])
    if np.isclose(abs(normal_dot_product), 1, atol=threshold):
        return 'parallel'
    elif np.isclose(normal_dot_product, 0, atol=threshold):
        return 'perpendicular'
    return 'none'


def distance_from_camera(point):
    return np.linalg.norm(point)

def remove_distant_clusters(filtered_points, filtered_labels, filtered_indices, max_distance):
    cleaned_points = []
    cleaned_labels = []
    cleaned_indices = []

    # Zamieniamy na numpy array, jeśli to konieczne
    filtered_points = np.array(filtered_points)
    filtered_labels = np.array(filtered_labels)
    filtered_indices = np.array(filtered_indices)

    for label in set(filtered_labels):
        mask = (filtered_labels == label)
        cluster_points = filtered_points[mask]
        cluster_indices = filtered_indices[mask]

        if len(cluster_points) == 0:
            continue

        centroid = np.mean(cluster_points, axis=0)
        distance_to_camera = np.linalg.norm(centroid)

        if distance_to_camera <= max_distance:
            cleaned_points.append(cluster_points)
            cleaned_labels.append(np.full(len(cluster_points), label))
            cleaned_indices.append(cluster_indices)

    if len(cleaned_points) > 0:
        cleaned_points = np.vstack(cleaned_points)
        cleaned_labels = np.concatenate(cleaned_labels)
        cleaned_indices = np.concatenate(cleaned_indices)
    else:
        cleaned_points = np.array([])
        cleaned_labels = np.array([])
        cleaned_indices = np.array([])

    return cleaned_points, cleaned_labels, cleaned_indices


def fit_cylinder(points, threshold=0.01):
    model = linear_model.RANSACRegressor()
    X = points[:, :2]
    y = points[:, 2]

    model.fit(X, y)
    inlier_mask = model.inlier_mask_

    inliers = points[inlier_mask]
    outliers = points[~inlier_mask]

    if len(inliers) > 0:
        center = np.mean(inliers, axis=0)
        radius = np.mean(np.linalg.norm(inliers[:, :2] - center[:2], axis=1))
        return center, radius, inliers

    return None

def evaluate_cylinder_fit(points, cylinder_center, cylinder_radius, threshold=0.005):
    distances = np.linalg.norm(points[:, :2] - cylinder_center[:2], axis=1)
    fitting_points = np.sum(np.abs(distances - cylinder_radius) < threshold)
    fitting_percentage = fitting_points / len(points)
    return fitting_percentage

def analyze_clusters(cluster_points, label, plane_model, filtered_labels, filtered_points, shapes_dict):
    cluster_cloud = o3d.geometry.PointCloud()
    cluster_cloud.points = o3d.utility.Vector3dVector(cluster_points)

    print(f"Analiza klastra {label}")
    current_cloud = cluster_cloud
    planes = [plane_model]
    perpendicular_planes_found = 0
    parallel_plane_found = False

    while perpendicular_planes_found < 2 and len(current_cloud.points) > 300:
        plane_model_next, inlier_next_cloud, outlier_next_cloud = segment_plane_and_extract(current_cloud)
        if plane_model_next is None:
            print(f"Klaster {label}: Nie udało się dopasować kolejnej płaszczyzny")
            break

        print(f"Klaster {label}: Dopasowano kolejną płaszczyznę o parametrach: {plane_model_next}")
        inlier_next_cloud.paint_uniform_color([random.random(), random.random(), random.random()])
        orientation = check_plane_orientation(plane_model_next, plane_model)

        if orientation == 'parallel' and not parallel_plane_found:
            print(f"Klaster {label}: Dopasowana płaszczyzna jest równoległa do podłogi.")
            parallel_plane_found = True
            planes.append(plane_model_next)
            current_cloud = outlier_next_cloud
            #o3d.visualization.draw_geometries([inlier_next_cloud, current_cloud])
        elif orientation == 'perpendicular' and perpendicular_planes_found < 2:
            print(f"Klaster {label}: Dopasowana płaszczyzna jest prostopadła do podłogi.")
            perpendicular_planes_found += 1
            planes.append(plane_model_next)
            current_cloud = outlier_next_cloud
            #o3d.visualization.draw_geometries([inlier_next_cloud, current_cloud])
        else:
            print(
                f"Klaster {label}: Dopasowana płaszczyzna nie jest prostopadła ani równoległa do podłogi. Pomijam.")
            current_cloud = outlier_next_cloud
            continue

    if parallel_plane_found and perpendicular_planes_found >= 1:
        shapes_dict[label] = "cubic"
        print(
            f"Klaster {label}: Wykryto prostopadłościan")
    else:
        print(
            f"Klaster {label}: Nie wykryto prostopadłościanu (nie znaleziono wymaganej liczby płaszczyzn)")

def fit_cone(points):

    if len(points) < 3:
        return None
    apex = points[0]
    other_points = points[1:]
    mean_point = np.mean(other_points, axis=0)
    direction = mean_point - apex
    norm_dir = np.linalg.norm(direction)
    if norm_dir < 1e-9:
        return None
    direction_vector = direction / norm_dir

    heights = []
    radii = []
    for p in other_points:
        ap = p - apex
        h = np.dot(ap, direction_vector)
        proj_point = apex + h * direction_vector
        r = np.linalg.norm(p - proj_point)
        if h > 1e-9:
            heights.append(h)
            radii.append(r)

    if len(heights) < 1:
        return None

    ratio = np.mean([r / h for r, h in zip(radii, heights) if h > 0])
    angle = np.arctan(ratio)

    return apex, direction_vector, angle


def ransac_cone(points, distance_threshold=0.01, num_iterations=500):

    if len(points) < 3:
        return None, []

    best_inliers = []
    best_model = None

    for _ in range(num_iterations):
        try:
            sample_indices = np.random.choice(points.shape[0], 3, replace=False)
            sample_points = points[sample_indices]
            cone_params = fit_cone(sample_points)
            if cone_params is None:
                continue
            apex, direction_vector, angle = cone_params
            angle_degrees = np.degrees(angle)
            if angle_degrees > 30:
                continue

            inliers = []
            tan_angle = np.tan(angle)
            for i, p in enumerate(points):
                ap = p - apex
                h = np.dot(ap, direction_vector)
                if h < 0:
                    continue
                proj_point = apex + h * direction_vector
                r = np.linalg.norm(p - proj_point)
                diff = abs(r - h * tan_angle)
                if diff < distance_threshold:
                    inliers.append(i)

            if len(inliers) > len(best_inliers):
                best_inliers = inliers
                best_model = (apex, direction_vector, angle)

                # Sprawdzamy inlier_percentage
                inlier_percentage = len(best_inliers) / len(points)
                print(inlier_percentage, "stozek")
                if inlier_percentage > 0.45:
                    break

        except Exception:
            continue

    return best_model, best_inliers

def highlight_selected_shape(pcd, filtered_points, filtered_labels, filtered_indices, outlier_indices,
      shapes_dict, selected_shape="rectangle", highlight_color=None, default_color=None):
    # Jeśli pcd nie ma kolorów, można je w razie potrzeby nadać przed wywołaniem funkcji
    # pcd.paint_uniform_color([1, 1, 1])  # gdyby była potrzeba jednolitego tła
    print("a")
    highlighted_cloud = o3d.geometry.PointCloud(pcd)
    all_points = np.asarray(highlighted_cloud.points)

    # Pobieramy oryginalne kolory
    all_colors = np.asarray(highlighted_cloud.colors)

    # Jeśli chmura nie ma kolorów, all_colors może być puste.
    # Wówczas można nadać jakiś domyślny kolor bazowy, np. biały:
    if len(all_colors) == 0:
        all_colors = np.ones((all_points.shape[0], 3))

    if highlight_color is None:
        highlight_color = [0, 0, 1.0]  # niebieski dla zaznaczonych figur

    for i, label in enumerate(filtered_labels):
        shape = shapes_dict.get(label, "none")
        if shape == selected_shape:
            original_index = outlier_indices[filtered_indices[i]]
            all_colors[original_index] = highlight_color

    highlighted_cloud.colors = o3d.utility.Vector3dVector(all_colors)
    o3d.visualization.draw_geometries([highlighted_cloud])


def analyze_point_cloud(folder: str):
    """
    Analizuje chmurę punktów, rozpoznaje figury geometryczne i wyświetla wyniki.

    Args:
        folder (str): Nazwa folderu z plikiem point_cloud.ply.

    Returns:
        dict: Czasy detekcji dla każdej figury.
        dict: Rozpoznane figury geometryczne.
        o3d.geometry.PointCloud: Połączona chmura punktów z podświetleniami.
    """
    pcd_path = f"result/{folder}/point_cloud.ply"
    pcd = o3d.io.read_point_cloud(pcd_path)

    if pcd.is_empty():
        print(f"Chmura punktów w folderze '{folder}' jest pusta.")
        return None, None, None

    # Segmentacja płaszczyzny (podłogi)
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
    inlier_cloud = pcd.select_by_index(inliers)
    outlier_cloud = pcd.select_by_index(inliers, invert=True)

    all_indices = np.arange(len(np.asarray(pcd.points)))
    outlier_indices = np.setdiff1d(all_indices, inliers)

    print(f"Parametry płaszczyzny: a: {plane_model[0]:.2f}, b: {plane_model[1]:.2f}, "
          f"c: {plane_model[2]:.2f}, d: {plane_model[3]:.2f}")

    points = np.asarray(outlier_cloud.points)

    # Klasteryzacja z użyciem HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=500, min_samples=10).fit(points)
    labels = clusterer.labels_
    unique_labels = set(labels)
    counts = np.bincount(labels[labels >= 0])

    print(
        f"Liczba wykrytych klastrów przed filtrowaniem szumu: {len(unique_labels) - (1 if -1 in unique_labels else 0)}")
    print(f"Minimalna liczba punktów w klastrach: {np.min(counts) if len(counts) > 0 else 0}")

    # Filtrowanie klastrów na podstawie minimalnej liczby punktów
    min_points_threshold = 15000
    valid_labels = [label for label, count in enumerate(counts) if count >= min_points_threshold]

    filtered_points = []
    filtered_labels = []
    filtered_indices = []
    shape_times = {
        'sphere': 0.0,
        'cylinder': 0.0,
        'cone': 0.0,
        'cubic': 0.0
    }

    for i, label in enumerate(labels):
        if label in valid_labels:
            filtered_points.append(points[i])
            filtered_labels.append(label)
            filtered_indices.append(i)

    filtered_points = np.array(filtered_points)

    # Odrzucanie klastrów na podstawie odległości od kamery
    max_distance = 1.0
    old_filtered_points = np.array(filtered_points)
    old_filtered_labels = np.array(filtered_labels)
    old_filtered_indices = np.array(filtered_indices)
    filtered_points, filtered_labels, filtered_indices = remove_distant_clusters(filtered_points, filtered_labels,
                                                                                 filtered_indices, max_distance)

    mask = []
    j = 0
    for i in range(len(old_filtered_points)):
        if j < len(filtered_points) and np.allclose(old_filtered_points[i], filtered_points[j]):
            mask.append(True)
            j += 1
        else:
            mask.append(False)
    mask = np.array(mask[:len(old_filtered_points)])
    filtered_indices = old_filtered_indices[mask]

    valid_labels = [label for label in valid_labels if label in filtered_labels]

    # Przygotowanie chmury punktów do wizualizacji
    colored_points = np.zeros((len(filtered_points), 3))
    cluster_colors = {label: [random.random(), random.random(), random.random()] for label in valid_labels}

    for i, label in enumerate(filtered_labels):
        colored_points[i] = cluster_colors[label]

    filtered_cloud = o3d.geometry.PointCloud()
    filtered_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    filtered_cloud.colors = o3d.utility.Vector3dVector(colored_points)

    filtered_cloud_cleaned = filtered_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)[0]
    floor_color = [0.0, 0.0, 1.0]
    inlier_cloud.colors = o3d.utility.Vector3dVector(np.tile(floor_color, (len(inlier_cloud.points), 1)))
    combined_cloud = inlier_cloud + filtered_cloud_cleaned

    #o3d.visualization.draw_geometries([combined_cloud])

    # Rozpoznawanie figur geometrycznych w klastrach
    shapes_dict = {}
    shape_times = {'sphere': 0.0, 'cone': 0.0, 'cylinder': 0.0, 'cubic': 0.0}

    for label in valid_labels:
        cluster_points = [filtered_points[i] for i in range(len(filtered_labels)) if filtered_labels[i] == label]
        cluster_cloud = o3d.geometry.PointCloud()
        cluster_cloud.points = o3d.utility.Vector3dVector(cluster_points)

        figure_found = False

        # Dopasowanie sfery
        try:
            print(f"Klaster {label}: Rozpoczynanie dopasowania sfery")
            start_time = time.time()
            sphere_model, sphere_inliers = ransac_sphere(np.asarray(cluster_cloud.points), distance_threshold=0.005,
                                                         num_iterations=5000)

            if sphere_model:
                center, radius = sphere_model
                inlier_percentage = len(sphere_inliers) / len(cluster_points)
                if inlier_percentage >= 0.75:
                    print(f"Klaster {label}: Dopasowano sferę o środku: {center}, promieniu: {radius}")
                    shapes_dict[label] = "sphere"
                    figure_found = True
                    shape_times['sphere'] += time.time() - start_time
                    continue

            shape_times['sphere'] += time.time() - start_time
        except Exception as e:
            print(f"Klaster {label}: Błąd podczas dopasowywania sfery: {e}")


        # Dopasowanie cylindra
        if not figure_found:
            print(f"Klaster {label}: Próba dopasowania cylindra")
            start_time = time.time()
            cylinder_result = fit_cylinder(np.array(cluster_points))

            if cylinder_result:
                center, radius, inliers = cylinder_result
                fitting_percentage = evaluate_cylinder_fit(np.array(cluster_points), center, radius)
                if fitting_percentage > 0.25:
                    print(f"Znaleziono cylinder w klastrze {label}. Środek: {center}, Promień: {radius}")
                    shapes_dict[label] = "cylinder"
                    figure_found = True

            shape_times['cylinder'] += time.time() - start_time

        # Dopasowanie stożka
        if not figure_found:
            print(f"Klaster {label}: Próba dopasowania stożka")
            start_time = time.time()
            cone_model, cone_inliers = ransac_cone(np.array(cluster_points), distance_threshold=0.005,
                                                   num_iterations=1000)

            if cone_model:
                apex, direction_vector, angle = cone_model
                inlier_percentage = len(cone_inliers) / len(cluster_points)
                if inlier_percentage >= 0.32:  # Próg akceptacji
                    print(
                        f"Znaleziono stożek w klastrze {label}. Wierzchołek: {apex}, Kąt: {np.degrees(angle):.2f} stopni")
                    shapes_dict[label] = "cone"
                    figure_found = True

            shape_times['cone'] += time.time() - start_time


        # Dopasowanie prostopadłościanu
        if not figure_found:
            print(f"Klaster {label}: Próba dopasowania prostopadłościanu")
            start_time = time.time()
            analyze_clusters(cluster_points, label, plane_model, filtered_labels, filtered_points, shapes_dict)
            shape_times['cubic'] += time.time() - start_time
            if shapes_dict.get(label) == "cubic":
                figure_found = True

    # Podświetlenie wybranej figury (opcjonalne)
   #highlight_selected_shape(pcd, filtered_points, filtered_labels, filtered_indices, outlier_indices,
    #                         shapes_dict, selected_shape="sphere", highlight_color=[0, 0, 1.0])
    print("=== Czas detekcji figur geometrycznych ===")
    for shape, duration in shape_times.items():
        print(f"{shape.capitalize()}: {duration:.2f} sekund")

    return shape_times, shapes_dict, pcd, filtered_points, filtered_labels, filtered_indices, outlier_indices

# highlight_selected_shape( pcd, filtered_points, filtered_labels, filtered_indices, outlier_indices,
#     shapes_dict, selected_shape="sphere", highlight_color=[0, 0, 1.0],  default_color=[0, 0, 0]
# )
#
# # Wyświetlenie czasu detekcji po przetworzeniu wszystkich klastrów
# print("=== Czas detekcji figur geometrycznych ===")
# for shape, duration in shape_times.items():
#     print(f"{shape.capitalize()}: {duration:.2f} sekund")

