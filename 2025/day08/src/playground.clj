(require '[clojure.string :as str]
         '[clojure.set :as set])

(defn parse-input [file]
  (->> file
       slurp
       str/split-lines
       (map #(str/split % #","))
       (map #(map parse-long %))))

(defn square [a]
  (* a a))

(defn dist-sq [a b]
  ;; square of the distance. square root is monotonic so unneccesery to sort distances
  [(reduce + (map #(square (- %1 %2)) a b)) a b])

(defn get-dist [pts]
  ;; returns all possible pairs of points and their distance
  (when (seq pts)
    (concat (map dist-sq (repeat (first pts)) (rest pts)) (get-dist (rest pts)))))

(defn shortest-connections [n pts]
  ;; returns the n shortest connections or all of them sorted if n=0
  (if (> n 0)
    (map rest (take n (sort (get-dist pts))))
    (map rest (sort (get-dist pts)))))

(defn connected-components [components paths]
  ;; returns all connected components with size > 1. Initialize with components=#{}. 
  (if (empty? paths)
    components
    (let [new-path (set (first paths))
          {non-occs true occs false} (group-by #(empty? (set/intersection new-path %)) components)]
      (connected-components (cons (apply set/union (cons new-path occs)) non-occs) (rest paths)))))

(defn until-connect-all [n components paths]
  ;; returns the path that results in a fully connected graph.
  (if (empty? paths)
    components
    (let [new-path (set (first paths))
          {non-occs true occs false} (group-by #(empty? (set/intersection new-path %)) components)
          new-components (cons (apply set/union (cons new-path occs)) non-occs)]
      (if (= n (count (first new-components)))
        new-path
        (recur n new-components (rest paths))))))


(defn count-connected-components [comps]
  ;; calculates the product of size of the three largest components
  (reduce * (take 3 (sort > (map count comps)))))


(defn part-a [n-con path]
  (->> path
       (parse-input)
       (shortest-connections n-con)
       (connected-components #{})
       (count-connected-components)))

(part-a 10 "../aoc/2025/day08/resources/test.txt")
(part-a 1000 "../aoc/2025/day08/resources/input.txt")

(defn part-b [path]
  (let [data (parse-input path)
        n (count data)]
    (->> data
         (shortest-connections 0)
         (until-connect-all n #{})
         (map first)
         (reduce *))))


(part-b "../aoc/2025/day08/resources/test.txt")
(part-b "../aoc/2025/day08/resources/input.txt")