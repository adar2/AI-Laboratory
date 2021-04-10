import matplotlib.pyplot as plt


def fill_list_with_last_value(lst: list, max_size: int):
    value = lst[-1]
    while len(lst) < max_size:
        lst.append(value)


if __name__ == '__main__':
    ga_costs = [3268, 3193, 3193, 3132, 3123, 3073, 3049, 3049, 2963, 2963, 2930, 2871, 2871, 2871, 2821, 2821, 2800, 2761, 2761, 2761,
                2695, 2688, 2688, 2688, 2658, 2645, 2620, 2620, 2534, 2534, 2514, 2514, 2514, 2503, 2482, 2482, 2459, 2459, 2423, 2423,
                2423, 2419, 2407, 2407, 2384, 2384, 2384, 2376, 2363, 2363, 2362, 2360, 2350, 2342, 2334, 2317, 2317, 2317, 2317, 2317,
                2317, 2311, 2292, 2277, 2277, 2277, 2270, 2270, 2263, 2263, 2263, 2263, 2246, 2246, 2246, 2215, 2215, 2215, 2215, 2215,
                2201, 2201, 2197, 2197, 2181, 2181, 2175, 2169, 2166, 2157, 2157, 2157, 2157, 2157, 2157, 2152, 2152, 2152, 2134, 2134,
                2134, 2130, 2125, 2110, 2110, 2095, 2095, 2095, 2095, 2095, 2095, 2092, 2092, 2078, 2078, 2078, 2078, 2078, 2077, 2070,
                2070, 2070, 2070, 2070, 2063, 2061, 2045, 2045, 2044, 2038, 2022, 2014, 2008, 2008, 2008, 2000, 2000, 2000, 2000, 2000,
                1993, 1993, 1988, 1988, 1988, 1982, 1982, 1981, 1981, 1977, 1959, 1959, 1959, 1959, 1959, 1959, 1953, 1953, 1953, 1952,
                1930, 1930, 1930, 1930, 1930, 1921, 1921, 1916, 1916, 1916, 1916, 1908, 1908, 1900, 1900, 1900, 1882, 1882, 1882, 1882,
                1882, 1870, 1870, 1870, 1870, 1863, 1863, 1863, 1860, 1852, 1852, 1852, 1852, 1852, 1852, 1849, 1849, 1849, 1834, 1834,
                1834, 1834, 1833, 1821, 1821, 1821, 1821, 1821, 1801, 1801, 1801, 1801, 1801, 1801, 1801, 1801, 1801, 1801, 1801, 1801,
                1801, 1801, 1801, 1801, 1795, 1795, 1795, 1795, 1795, 1791, 1791, 1785, 1785, 1785, 1785, 1780, 1780, 1768, 1768, 1768,
                1768, 1768, 1767, 1767, 1767, 1767, 1757, 1757, 1757, 1757, 1754, 1754, 1754, 1754, 1752, 1734, 1734, 1734, 1734, 1722,
                1722, 1722, 1722, 1722, 1715, 1715, 1715, 1715, 1708, 1708, 1708, 1708, 1708, 1707, 1707, 1707, 1707, 1707, 1707, 1707,
                1706, 1706, 1701, 1701, 1701, 1701, 1701, 1699, 1699, 1699, 1699, 1699, 1699, 1699, 1699, 1699, 1698, 1698, 1698, 1698,
                1698, 1698, 1698, 1698, 1698, 1689, 1689, 1689, 1689, 1689, 1686, 1686, 1686, 1686, 1686, 1686, 1681, 1681, 1681, 1675,
                1675, 1675, 1675, 1675, 1675, 1675, 1673, 1673, 1673, 1665, 1665, 1665, 1665, 1665, 1663, 1641, 1641, 1641, 1641, 1641,
                1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1641, 1639,
                1639, 1639, 1639, 1639, 1639, 1639, 1639, 1639, 1639, 1634, 1634, 1634, 1634, 1634, 1634, 1634, 1634, 1634, 1634, 1634,
                1634, 1634, 1634, 1634, 1634, 1627, 1624, 1615, 1615, 1615, 1614, 1609, 1609, 1609, 1609, 1604, 1604, 1602, 1602, 1602,
                1599, 1599, 1598, 1598, 1596, 1596, 1592, 1592, 1592, 1592, 1592, 1592, 1592, 1592, 1592, 1592, 1592, 1592, 1580, 1580,
                1580, 1580, 1580, 1580, 1580, 1580, 1580, 1580, 1580, 1580, 1580, 1580, 1573, 1573, 1573, 1573, 1573, 1573, 1573, 1573,
                1573, 1573, 1573, 1573, 1573, 1573, 1573, 1573, 1573, 1573, 1573, 1573, 1573, 1567, 1567, 1567, 1567, 1567, 1567, 1567,
                1567, 1567, 1567, 1567, 1567, 1567, 1567, 1567, 1567, 1560, 1560, 1560, 1560, 1560, 1560, 1560, 1560, 1560, 1560, 1560,
                1560, 1559, 1559, 1559, 1559, 1559, 1559, 1559, 1559, 1559, 1559, 1559, 1556, 1556, 1556, 1556, 1556, 1556, 1556, 1556,
                1556, 1556, 1554, 1554, 1554, 1549, 1549, 1549, 1549, 1549, 1549, 1548, 1548, 1548, 1548, 1544, 1541, 1541, 1541, 1541,
                1541, 1532, 1532, 1532, 1532, 1532, 1532, 1529, 1529, 1529, 1529, 1529, 1529, 1526, 1526, 1526, 1524, 1524, 1524, 1524,
                1524, 1524, 1524, 1524, 1524, 1515, 1515, 1515, 1515, 1515, 1515, 1515, 1515, 1515, 1515, 1515, 1508, 1508, 1508, 1508,
                1508, 1508, 1508, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1497, 1497, 1495, 1495, 1495, 1491, 1491, 1491, 1484, 1484,
                1484, 1484, 1484, 1484, 1484, 1484, 1484, 1484, 1484, 1484, 1484, 1484, 1484, 1484, 1481, 1481, 1481, 1481, 1481, 1481,
                1481, 1481, 1481, 1479, 1479, 1479, 1479, 1479, 1479, 1475, 1475, 1475, 1475, 1475, 1475, 1475, 1475, 1475, 1475, 1470,
                1470, 1470, 1470, 1470, 1470, 1470, 1470, 1470, 1470, 1470, 1470, 1470, 1470, 1470, 1470, 1470, 1459, 1459, 1459, 1459,
                1459, 1459, 1459, 1452, 1452, 1452, 1449, 1449, 1449, 1449, 1449, 1440, 1440, 1440, 1440, 1440, 1433, 1433, 1433, 1433,
                1433, 1430, 1430, 1426, 1426, 1426, 1426, 1426, 1419, 1419, 1419, 1419, 1419, 1419, 1419, 1419, 1419, 1419, 1418, 1418,
                1418, 1418, 1418, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417, 1417,
                1417, 1417, 1417, 1416, 1416, 1416, 1416, 1416, 1406, 1406, 1406, 1406, 1406, 1406, 1406, 1397, 1397, 1397, 1397, 1397,
                1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1397, 1396, 1396, 1396,
                1396, 1396, 1396, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394,
                1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394, 1394,
                1394, 1394, 1394, 1394, 1389, 1389, 1389, 1389, 1389, 1389, 1389, 1389, 1389, 1389, 1389, 1389, 1389, 1389, 1389, 1389,
                1389, 1389, 1389, 1389, 1389, 1389, 1389, 1386, 1386, 1386, 1386, 1386, 1386, 1386, 1386, 1379, 1379, 1379, 1379, 1379,
                1379, 1379, 1379, 1379, 1379, 1378, 1378, 1377, 1377, 1371, 1371, 1371, 1365, 1365, 1365, 1359, 1359, 1359, 1359, 1359,
                1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359, 1359,
                1359, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355,
                1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355,
                1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355,
                1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1355, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353,
                1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353,
                1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1353, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349,
                1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349, 1349]

    ts_costs = [1386, 1343, 1342, 1335, 1332, 1329, 1322, 1322, 1319, 1314, 1308, 1308, 1308, 1308, 1306, 1306, 1304, 1304, 1298, 1298, 1298, 1297, 1297, 1291, 1284, 1284, 1270, 1270, 1266, 1266, 1266, 1265, 1265, 1265, 1265, 1264, 1264, 1262, 1243, 1243, 1243, 1235, 1235, 1235, 1235, 1235, 1235, 1228, 1228, 1228, 1228, 1228, 1228, 1228, 1228, 1228, 1228, 1228, 1228, 1228, 1227, 1227, 1227, 1227, 1223, 1223, 1223, 1222, 1216, 1216, 1216, 1216, 1216, 1214, 1214, 1214, 1214, 1214, 1214, 1214, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1213, 1206, 1206, 1206, 1206, 1206, 1206, 1206, 1206, 1206, 1206, 1206, 1206, 1206, 1206, 1204, 1204, 1204, 1204, 1204, 1204, 1204, 1204, 1204, 1204, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1201, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1199, 1199, 1199, 1199, 1199, 1199, 1199, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197, 1197]

    aco_costs = [1423, 1372, 1367, 1343, 1327, 1327, 1327, 1327, 1327, 1327, 1327, 1327, 1327, 1327, 1327, 1327, 1327, 1327, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242, 1242]

    sa_costs = [1386, 1380, 1376, 1373, 1340, 1329, 1319, 1316, 1315, 1315, 1315, 1315, 1315, 1315, 1315, 1291, 1289, 1285, 1285, 1285, 1283, 1279, 1279, 1279, 1279, 1279, 1277, 1275, 1267, 1262, 1262, 1257, 1251, 1248, 1248, 1248, 1248, 1248, 1248, 1246, 1246, 1246, 1245, 1245, 1242, 1241, 1238, 1232, 1232, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1223, 1220, 1217, 1215, 1213, 1210, 1207, 1203, 1203, 1203, 1203, 1203, 1203, 1203, 1203, 1203, 1203, 1199, 1198, 1198, 1198, 1198, 1198, 1198, 1198, 1196, 1196, 1196, 1196, 1196, 1194, 1194, 1192, 1191, 1191, 1191, 1190, 1190, 1190, 1190, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1189, 1187, 1184, 1184, 1179, 1179, 1179, 1179, 1177, 1177, 1177, 1177, 1177, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1173, 1173, 1173, 1173, 1173, 1173, 1173, 1173, 1171, 1171, 1171, 1170, 1170, 1170, 1170, 1170, 1170, 1170, 1169, 1168, 1166, 1166, 1163, 1163, 1163, 1163, 1163, 1163, 1161, 1161, 1161, 1161, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1160, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1159, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1158, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1157, 1156, 1156, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1153, 1150, 1150, 1150, 1150, 1150, 1150, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146, 1146]
    max_list_length = max(len(ts_costs), len(ga_costs), len(sa_costs), len(aco_costs))
    fill_list_with_last_value(ts_costs, max_list_length)
    fill_list_with_last_value(ga_costs, max_list_length)
    fill_list_with_last_value(aco_costs, max_list_length)
    fill_list_with_last_value(sa_costs, max_list_length)
    iterations = range(max_list_length)
    plt.plot(iterations, ts_costs)
    plt.plot(iterations, ga_costs)
    plt.plot(iterations, aco_costs)
    plt.plot(iterations, sa_costs)
    plt.legend(["TS", "GA", "ACO", "SA"])
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.title("Costs Per Iteration: n101-k14")
    plt.show()
