class NISOC:

    def execute(self):
        lablelist = {i: {i: 1} for i in self._G.nodes()}

        for t in range(self._T):
            # 根据 NI_FN 排序并优先处理
            visitlist = sorted(self._G.nodes(), key=lambda x: -self._ni_fn_values[x])

            for visit in visitlist:
                temp_count = 0
                temp_label = {}
                total = len(self._G[visit])

                for i in self._G.neighbors(visit):
                    weight = label_weight(self._G, i, visit, self._similarity_matrix, self._node_to_index,
                                          self._ni_fn_values)
                    res = {key: value / total * weight for key, value in lablelist[i].items()}
                    temp_label = dict(Counter(res) + Counter(temp_label))

                temp_count = len(temp_label)
                temp_label2 = temp_label.copy()
                for key, value in list(temp_label.items()):
                    if value < 1 / self._v:
                        del temp_label[key]
                        temp_count -= 1

                if temp_count == 0:
                    if temp_label2:
                        b = random.sample(list(temp_label2.keys()), 1)
                        temp_label = {b[0]: 1}
                    else:
                        neighbor_labels = [label for neighbor in self._G.neighbors(visit) for label in
                                           lablelist[neighbor].keys()]
                        if neighbor_labels:
                            b = random.sample(neighbor_labels, 1)
                            temp_label = {b[0]: 1}
                        else:
                            temp_label = {visit: 1}
                else:
                    tsum = sum(temp_label.values())
                    temp_label = {key: value / tsum for key, value in temp_label.items()}

                lablelist[visit] = temp_label

        communities = collections.defaultdict(lambda: list())
        # 扫描lablelist中的记录标签，相同标签的节点加入同一个社区中
        for primary, change in lablelist.items():
            for label in change.keys():
                communities[label].append(primary)
        # 返回值是个数据字典，value以集合的形式存在
        return communities.values(), lablelist