import csv_parser
import python
plt = python.module("matplotlib.pyplot")

graph_counter = 0
OUTPUT_PATH = "output"

fun read_csv(path:String, ... int_indicies) {
    res = with_open(path, csv_parser.dict_reader)
    for (it: res) {
        for (key, v: it) {
            it[key] = v.replace("\\n", " ")
        }
    }
    for (key: int_indicies) {
        for (it: res) {
            it[key] = Int(it[key])
        }
    }
    return res
}

fun plot_hist(x, title:String) {
    ~plt.hist(x)
    ~plt.xlabel("Value")
    ~plt.ylabel("Frequency")
    ~plt.title(title)
    name = f"graph_{::graph_counter}.png"
    ::graph_counter += 1
    ~plt.savefig(::OUTPUT_PATH++"/"++name)
    return Note(f"![title]({name})\n", "md")
}

@main
fun main() {
    if (args.length() != 1) {
        ~print("Usage: moss analysis.ms <path to data folder>")
        ~exit(1)
    }
    data_path = args[0]
    cards_path = data_path++"/cards.csv"

    md"""
# Card analysis
"""

    cards = read_csv(cards_path, "Hodnota")
    plot_hist([i["Hodnota"] : i = cards], "Card value distribution")

    md"""## Cards
"""

    // Output csvs as tables
    Note(with_open(cards_path, fun(f)=f.read()), "csv")
}