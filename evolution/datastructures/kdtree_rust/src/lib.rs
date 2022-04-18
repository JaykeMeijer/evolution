use pyo3::prelude::*;

#[derive(Clone, Copy)]
pub struct Rect {
    top: i32,
    left: i32,
    width: i32,
    height: i32,
}

#[pyclass]
#[derive(Clone, Copy)]
pub struct KDTreePoint {
    #[pyo3(get, set)]
    x: i32,
    #[pyo3(get, set)]
    y: i32,
    #[pyo3(get, set)]
    object_id: i32,
}

#[pyclass]
#[derive(Clone)]
pub struct KDTree {
    area: Rect,
    depth: i32,
    vertical: bool,
    left: Option<Box<KDTree>>,
    right: Option<Box<KDTree>>,
    point: Option<Box<KDTreePoint>>,
}

impl Rect {
    pub fn new(area: (i32, i32, i32, i32)) -> Rect {
        let (top, left, height, width) = area;
        Rect {
            top,
            left,
            height,
            width,
        }
    }
    pub fn string(&self) -> String {
        let top = self.top;
        let left = self.left;
        let bottom = top + self.height;
        let right = left + self.width;
        return format!("Rect from ({top}, {left}) to ({bottom}, {right})");
    }
}

#[pymethods]
impl KDTreePoint {
    #[new]
    pub fn new(x: i32, y: i32, object_id: i32) -> KDTreePoint {
        KDTreePoint { x, y, object_id }
    }
    pub fn string(&self) -> String {
        return format!("Object {} at ({}, {})", self.object_id, self.x, self.y);
    }
}

#[pymethods]
impl KDTree {
    #[new]
    pub fn new(area: (i32, i32, i32, i32), points: Vec<KDTreePoint>) -> KDTree {
        let mut tree = KDTree {
            area: Rect::new(area),
            depth: 0,
            vertical: true,
            left: None,
            right: None,
            point: None,
        };
        tree.insert_points(points);
        return tree;
    }
    pub fn string(&self) -> String {
        let output: String = format!("Tree of depth {} at {}. ", self.depth, self.area.string());
        let output_point = if self.point.is_none() {
            format!("Point is not set.")
        } else {
            format!("Point is {}", self.point.as_ref().unwrap().string())
        }
        .to_string();
        let left_string = if self.left.is_none() {
            format!("")
        } else {
            format!("\t\nLeft: {}", self.left.as_ref().unwrap().string())
        };
        let right_string = if self.right.is_none() {
            format!("")
        } else {
            format!("\t\nRight: {}", self.right.as_ref().unwrap().string())
        };
        return output + &output_point + &left_string + &right_string;
    }
    pub fn find_nearest_neighbour(&self, location: (i32, i32), obj: i32) -> (i32, f64) {
        let (point, distance) = self.find_nearest_neighbour_recursive(location, obj, i32::MAX, -1);
        return (point, f64::from(distance).sqrt());
    }
}

impl KDTree {
    fn new_internal(area: Rect, depth: i32, points: Vec<KDTreePoint>, vertical: bool) -> KDTree {
        let mut tree = KDTree {
            area: area,
            depth: depth,
            vertical: vertical,
            left: None,
            right: None,
            point: None,
        };
        tree.insert_points(points);
        return tree;
    }
    fn insert_points(&mut self, mut points: Vec<KDTreePoint>) {
        if points.len() == 1 {
            self.point = Some(Box::new(points[0]));
            return;
        }

        if self.vertical {
            points.sort_by_key(|d| d.x);
        } else {
            points.sort_by_key(|d| d.y);
        }

        let median: usize = points.len() / 2;
        let median_point = points[median];
        self.point = Some(Box::new(median_point));
        let left_points: Vec<KDTreePoint> = points[..median].to_vec();
        let right_points: Vec<KDTreePoint> = points[median + 1..].to_vec();

        if left_points.len() > 0 {
            self.left = Some(Box::new(KDTree::new_internal(
                self.left_rect(median_point),
                self.depth + 1,
                left_points,
                !(self.vertical),
            )));
        }
        if right_points.len() > 0 {
            self.right = Some(Box::new(KDTree::new_internal(
                self.right_rect(median_point),
                self.depth + 1,
                right_points,
                !(self.vertical),
            )));
        }
    }
    fn left_rect(&self, point: KDTreePoint) -> Rect {
        if self.vertical {
            return Rect {
                left: self.area.left,
                top: self.area.top,
                width: point.x - self.area.left,
                height: self.area.height,
            };
        } else {
            return Rect {
                left: self.area.left,
                top: self.area.top,
                width: self.area.width,
                height: point.y - self.area.top,
            };
        }
    }
    fn right_rect(&self, point: KDTreePoint) -> Rect {
        if self.vertical {
            return Rect {
                left: point.x,
                top: self.area.top,
                width: (self.area.left + self.area.width) - point.x,
                height: self.area.height,
            };
        } else {
            return Rect {
                left: self.area.left,
                top: point.y,
                width: self.area.width,
                height: (self.area.top + self.area.height) - point.y,
            };
        }
    }
    fn find_nearest_neighbour_recursive(
        &self,
        location: (i32, i32),
        obj: i32,
        current_best: i32,
        best_node: i32,
    ) -> (i32, i32) {
        let point: &KDTreePoint = self.point.as_ref().unwrap();
        let new_left: Option<Box<KDTree>> = self.left.clone();
        let new_right: Option<Box<KDTree>> = self.right.clone();
        if obj != point.object_id {
            let (next_tree, other_tree) = if self.left_next(location, (point.x, point.y)) {
                (new_left, new_right)
            } else {
                (new_right, new_left)
            };
            let local_dist = square_dist((point.x, point.y), location);
            return self.handle_tree(
                location,
                obj,
                next_tree,
                other_tree,
                local_dist,
                current_best,
                best_node,
            );
        } else {
            let (best_node_1, current_best_1) = self.handle_tree(
                location,
                obj,
                new_left,
                new_right,
                0,
                current_best,
                best_node,
            );
            let new_left: Option<Box<KDTree>> = self.left.clone();
            let new_right: Option<Box<KDTree>> = self.right.clone();
            let (best_node_2, current_best_2) = self.handle_tree(
                location,
                obj,
                new_left,
                new_right,
                0,
                current_best,
                best_node,
            );
            if current_best_1 < current_best_2 {
                return (best_node_1, current_best_1);
            } else {
                return (best_node_2, current_best_2);
            }
        }
    }
    fn left_next(&self, location: (i32, i32), split_point: (i32, i32)) -> bool {
        if self.vertical {
            return location.0 < split_point.0;
        } else {
            return location.0 < split_point.1;
        }
    }
    fn handle_tree(
        &self,
        location: (i32, i32),
        obj: i32,
        next_tree: Option<Box<KDTree>>,
        other_tree: Option<Box<KDTree>>,
        local_dist: i32,
        current_best: i32,
        best_node: i32,
    ) -> (i32, i32) {
        match next_tree {
            Some(p) => {
                return self.handle_non_leave(
                    location,
                    obj,
                    p,
                    other_tree,
                    local_dist,
                    current_best,
                    best_node,
                )
            }
            None => return self.handle_leave(obj, local_dist, current_best, best_node),
        }
    }
    fn handle_leave(
        &self,
        obj: i32,
        local_dist: i32,
        current_best: i32,
        best_node: i32,
    ) -> (i32, i32) {
        let point: &KDTreePoint = self.point.as_ref().unwrap();
        if local_dist < current_best && point.object_id != obj {
            return (point.object_id, local_dist);
        } else {
            return (best_node, current_best);
        }
    }
    fn handle_non_leave(
        &self,
        location: (i32, i32),
        obj: i32,
        next_tree: Box<KDTree>,
        other_tree: Option<Box<KDTree>>,
        local_dist: i32,
        current_best: i32,
        best_node: i32,
    ) -> (i32, i32) {
        let point: &KDTreePoint = self.point.as_ref().unwrap();
        let (mut best_node, mut current_best) =
            next_tree.find_nearest_neighbour_recursive(location, obj, current_best, best_node);

        if local_dist < current_best && point.object_id != obj {
            current_best = local_dist;
            best_node = point.object_id;
        }

        let distance_to_plane: i32 = if self.vertical {
            (location.0 - point.x).abs()
        } else {
            (location.1 - point.y).abs()
        };

        if distance_to_plane.pow(2) < current_best && !other_tree.is_none() {
            return other_tree.unwrap().find_nearest_neighbour_recursive(
                location,
                obj,
                current_best,
                best_node,
            );
        } else {
            return (best_node, current_best);
        }
    }
}

fn square_dist(point_a: (i32, i32), point_b: (i32, i32)) -> i32 {
    return (point_a.0 - point_b.0).pow(2) + (point_a.1 - point_b.1).pow(2);
}

#[pymodule]
fn rust_kdtree(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<KDTreePoint>()?;
    m.add_class::<KDTree>()?;
    Ok(())
}
