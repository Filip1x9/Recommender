import _sqlite3
import datetime
import math
import statistics


def pearson(item1, item2):
    mean1 = statistics.mean(item1.values())
    mean2 = statistics.mean(item2.values())

    up = 0
    down1 = 0
    down2 = 0

    for user in item1.keys():
        if user in item2:
            up += (item1[user] - mean1) * (item2[user] - mean2)
            down1 += (item1[user] - mean1) ** 2
            down2 += (item2[user] - mean2) ** 2

    if down1 * down2 == 0:
        return 0

    return up / (math.sqrt(down1) * math.sqrt(down2))


def select_user_rating_for_item(item):
    cursor.execute("select user,rating from Training where item='" + item + "'")

    return {e[0]: float(e[1]) for e in cursor.fetchall()}


connection = _sqlite3.connect("comp3208-small.db")
cursor = connection.cursor()


def predict():
    file = open("predictions.csv", "w")
    k = 0

    cursor.execute("select * from Testing")
    to_predict = cursor.fetchall()

    database = {}
    sim_database = {}

    for entry in to_predict:

        # 1.1. Get users that have rated the item entry[1] (item that user entry[0] has rated)
        cursor.execute("select item, rating from Training where user='" + entry[0] + "'")
        sim = cursor.fetchall()

        if not entry[1] in database:
            database[entry[1]] = select_user_rating_for_item(entry[1])

        if len(database[entry[1]]) != 0:
            # 1.2. Calculate pearson P and select first N (5,10,..) users that have a positive correlation
            similarity = []
            i = 0
            while len(similarity) < 5:
                # failsafe
                if i == len(sim):
                    break

                if sim[i][0] not in database:
                    database[sim[i][0]] = select_user_rating_for_item(sim[i][0])

                u1 = entry[1]
                u2 = sim[i][0]

                if u1 > u2:
                    aux = u1
                    u1 = u2
                    u2 = aux

                pair = (u1, u2)
                if pair not in sim_database:
                    sim_database[pair] = pearson(database[u1], database[u2])
                # else:
                #     print("useful!!!!!!!!!!!")

                if sim_database[pair] > 0:
                    similarity.append(sim_database[pair])
                i += 1

            # 1.3. Calculate predicted rating using formula
            mark = statistics.mean(database[entry[1]].values())
            numerator = 0
            denominator = 0

            # print(len(similarity))
            for i in range(len(similarity)):
                r_mean = statistics.mean(database[sim[i][0]].values())
                numerator = numerator + similarity[i] * (float(sim[i][1]) - r_mean)
                denominator = denominator + similarity[i]

            if denominator != 0:
                mark = mark + numerator / denominator

            k += 1
            print(k, entry, mark)
            file.write(entry[0] + "," + entry[1] + "," + str(mark) + "\n")

    file.close()


predict()

connection.close()
