(System/getProperty "user.dir")
(require '[clojure.string :as str])

(def raw-data (->
               "../aoc/2025/day01/resources/input.txt"
               slurp
               (str/split #"\r\n")))

(defn parse-move [[_ direction number]]
  (* (case direction
       "L" -1
       "R" 1)
     (Integer/parseInt number)))

(def parsed-data
  (map #(parse-move (re-matches #"(R|L)([0-9]*)" %)) raw-data))

(defn next-turn [[acc zland zpassed] next]
  (let [new-acc (mod (+ acc next) 100)]
    [new-acc
     (if (zero? new-acc) (inc zland) zland)
     (+ zpassed (abs (Math/floorDiv (+ acc next) 100)))]))

(reduce next-turn [50 0 0] parsed-data)