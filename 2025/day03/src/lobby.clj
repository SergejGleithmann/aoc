(require '[clojure.string :as str])

(def raw-data (->
               "../aoc/2025/day03/resources/input.txt"
               slurp
               str/split-lines))

(def parsed-data
  (->>
   raw-data
   (map #(str/split % #""))))

(take 3 parsed-data)

(defn max-jolt [[x y] x]
  ())