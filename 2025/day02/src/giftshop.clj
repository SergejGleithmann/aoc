(require '[clojure.string :as str])

(def raw-data (->
               "../aoc/2025/day02/resources/input.txt"
               slurp
               (str/split #",")))

(defn parse-range [s]
  (apply range (map #(bigint %) (str/split s #"-"))))

(def parsed-data
  (->> raw-data
       (map parse-range)
       (apply concat)))

(defn split-half [s]
  (let [mid (quot (.length s) 2)]
    [(subs s 0 mid)
     (subs s mid)]))

(defn split-all [s]
  (let [possible-splits (filter
                         #(= 0 (mod (.length s) %))
                         (range 1 (.length s)))]
    (map #(partition % s) possible-splits)))

(defn illegal-a? [x]
  (apply = (split-half (str x))))

(defn illegal-b? [x]
  (some true? (map #(apply = %) (split-all (str x)))))


(reduce + (filter illegal-a? parsed-data))
(reduce + (filter illegal-b? parsed-data))