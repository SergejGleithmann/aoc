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
  (when (seq coll)
    (let [[valid rest] (split-with (complement pred) coll)
          todo (drop-while pred rest)]
      (cons valid (split-at-pred pred todo)))))

(defn parse-input-vertical [path]
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
              (map str/join)
              (map str/trim)
              (map parse-long)
              (split-at-pred nil?))]
    [ops nums]))

(defn sum-file [parser calc-fn path]
  (->> path
       parser
       calc-fn
       (reduce +)))

(sum-file parse-input calc "../aoc/2025/day06/resources/test.txt")
(sum-file parse-input calc "../aoc/2025/day06/resources/input.txt")
(sum-file parse-input-vertical calc-2 "../aoc/2025/day06/resources/test.txt")
(sum-file parse-input-vertical calc-2 "../aoc/2025/day06/resources/input.txt")