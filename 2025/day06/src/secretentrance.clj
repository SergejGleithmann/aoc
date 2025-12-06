(require '[clojure.string :as str])

(defn parse-op [op]
  (case op
    "*" *
    "+" +))

(defn calc [data]
  (map #(apply (parse-op (last %)) (map parse-long (butlast %))) (apply map vector data)))

(defn parse-input [path]
  (let [raw (->
             path
             slurp
             (str/split #"\r\n"))]
    (->> raw
         (map str/trim)
         (map #(str/split % #" +")))))

(defn calc-2 [[fs args]]
  (map apply fs args))

(defn split-at-pred [pred coll]
  (if (empty? coll)
    coll
    (let [[valid rest] (split-with (complement pred) coll)
          todo (drop-while pred rest)]
      (cons valid (split-at-pred pred todo)))))

(defn parse-input-2 [path]
  (let [raw (->
             path
             slurp
             (str/split #"\r\n"))
        ops (map parse-op (str/split (last raw) #" +"))
        nums (->>
              raw
              butlast
              (map #(str/split % #""))
              (apply map vector)
              (map #(apply str %))
              (map str/trim)
              (map parse-long)
              (split-at-pred nil?))]
    [ops nums]))

(->> "../aoc/2025/day06/resources/test.txt"
     parse-input
     calc
     (reduce +))

(->> "../aoc/2025/day06/resources/input.txt"
     parse-input
     calc
     (reduce +))

(->> "../aoc/2025/day06/resources/test.txt"
     parse-input-2
     calc-2
     (reduce +))

(->> "../aoc/2025/day06/resources/input.txt"
     parse-input-2
     calc-2
     (reduce +))