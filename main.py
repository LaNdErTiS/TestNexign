class Node:
    def __new__(cls, max_freq, is_list, value, children=None, parent=None, *args, **kwargs):
        instance = super(Node, cls).__new__(cls, *args, **kwargs)
        return instance

    def __init__(self, orig_freq, is_list, value, parent=None, children=None):
        self.orig_freq = orig_freq
        self.max_freq = orig_freq
        self.is_list = is_list
        self.value = value
        self.parent = parent
        if children is None:
            self.children = []

    def list_dfs(self, visited_nodes, visited_list):
        if self not in visited_nodes:
            visited_nodes.append(self)
            if self.is_list:
                visited_list.append(self)
            for el in self.children:
                el.list_dfs(visited_nodes, visited_list)

    def insert(self, node_new):
        self.children.append(node_new)

    def substring_search(self, string, flag=False):
        found_root_node = self
        for symbol in range(len(string)):
            was_founded = False
            for el in found_root_node.children:
                if string[symbol] == el.value:
                    found_root_node = el
                    symbol += 1
                    was_founded = True
                    break
            if not was_founded:
                return found_root_node, symbol
        if flag:
            found_root_node.is_list = True
        return found_root_node, len(string)

    def update_max_freq(self, freq_new):
        self.max_freq = freq_new
        if self.parent is not None:
            self.parent.update_max_freq(freq_new)

    def update_freq(self, freq_new):
        self.orig_freq = freq_new

    def became_the_word(self):
        variable_node = self
        result_word = ""
        while variable_node.parent is not None:
            result_word = variable_node.value + result_word
            variable_node = variable_node.parent
        return result_word

    def find_top_frequency_word(self):
        arr_of_list = []
        set_of_frequency = set()
        dict_of_word = {}
        visited_nodes = []
        self.list_dfs(visited_nodes, arr_of_list)
        for node in arr_of_list:
            letter = node.became_the_word()
            frequency = node.orig_freq
            if dict_of_word.get(frequency) is None:
                dict_of_word[frequency] = []
            dict_of_word[frequency].append(letter)
            set_of_frequency.add(frequency)
        list_of_frequency = sorted(set_of_frequency)
        list_of_frequency.reverse()

        number_of_top = 0
        for node in list_of_frequency:
            temp_arr = dict_of_word[node]
            temp_arr.sort()
            for top_word in temp_arr:
                if number_of_top > 9:
                    break
                else:
                    print(top_word)
                    number_of_top += 1
            if number_of_top > 9:
                break


if __name__ == "__main__":
    root_node = Node(100, False, "")
    old_root_node = root_node
    counter = int(input())

    for i in range(counter):
        new_value, new_freq = input().split(' ')
        new_freq = int(new_freq)
        root_node_for_insert, string_position = old_root_node.substring_search(new_value, True)
        j = string_position
        if root_node_for_insert is not None:
            root_node = root_node_for_insert
            if j == len(new_value):
                root_node.update_freq(new_freq)
                continue
        while j < len(new_value):
            if j == len(new_value) - 1:
                new_node = Node(new_freq, True, new_value[j], root_node)
                root_node.insert(new_node)
            else:
                new_node = Node(new_freq, False, new_value[j], root_node)
                root_node.insert(new_node)
            j += 1
            root_node = new_node
        root_node = old_root_node

    list_of_words = []
    counter = int(input())
    for i in range(counter):
        word = input()
        list_of_words.append(word)

    for i in range(len(list_of_words)):
        root_node_for_search, string_position = old_root_node.substring_search(list_of_words[i])
        if old_root_node != root_node_for_search:
            root_node_for_search.find_top_frequency_word()
        if i != len(list_of_words) - 1:
            print()
