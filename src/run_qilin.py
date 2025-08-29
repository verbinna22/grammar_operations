from datetime import datetime
from os import system
from pathlib import Path


FOLDER_WITH_GRAPHS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs"
FOLDER_WITH_BENCHMARKS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers_example/src"
FOLDER_WITH_QILIN : str = "/mnt/data/MyOwnFolder/learning/p_algo/Qilin"


def main() -> None:
    graphs = Path(FOLDER_WITH_GRAPHS)
    benchmarks = Path(FOLDER_WITH_BENCHMARKS)
    for graph in graphs.iterdir():
        if ord(graph.name[0]) >= ord('j') or graph.name in {"com_fasterxml_jackson"}:
            continue
        else:
            print(graph)
            benchmark = (benchmarks / graph.name).glob('**/*.java',)
            for filename in benchmark:
                print(filename)
                name = filename.name.removesuffix(".java")
                initial_time = datetime.now()
                command : str = fr'''
                /bin/bash -c "\
                cd {FOLDER_WITH_QILIN} && java -cp ./artifact/Qilin-0.9.7-SNAPSHOT.jar:/mnt/data/MyOwnFolder/learning/p_algo/logback-classic-1.3.0.jar driver.Main  -pae -pe -clinit=ONFLY -lcs -mh -pta=1c -apppath /mnt/data/MyOwnFolder/entertaiment/java/classes/{graph.name}.jar -jre=/mnt/data/MyOwnFolder/learning/p_algo/Qilin/artifact/benchmarks/JREs/jre1.6.0_45 -mainclass {graph.name}.{name} -dumppts && cp /mnt/data/MyOwnFolder/learning/p_algo/Qilin/sootOutput/pts.txt {graph / f"result_qilin_{name}.txt"}"\
                '''
                # print(command)
                system(command)
                with open(graph / f"time_to_qilin_{name}.txt", mode='w', encoding='utf-8') as file:
                    file.write(f"{datetime.now() - initial_time}\n")


if __name__ == "__main__":
    main()

# /mnt/data/MyOwnFolder/learning/p_algo/jdk8u462-b08
# soot.Scene.getMethod
# cd "/mnt/data/MyOwnFolder/learning/p_algo/Qilin" && /home/nikita/.jdks/ms-17.0.16/bin/java -cp ./artifact/Qilin-0.9.7-SNAPSHOT.jar:/mnt/data/MyOwnFolder/learning/p_algo/logback-classic-1.3.0.jar driver.Main  -pae -pe -clinit=ONFLY -lcs -mh -pta=1c -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-core-2.19.2-sources.jar -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-annotations-3.0-rc5-sources.jar  -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-databind-2.19.2.jar -jre=/mnt/data/MyOwnFolder/learning/p_algo/jdk8u462-b08 -dumppts && cp /mnt/data/MyOwnFolder/learning/p_algo/Qilin/sootOutput/pts.txt /mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs/result_qilin_jackson.txt
# cd "/mnt/data/MyOwnFolder/learning/p_algo/Qilin" && java -cp ./artifact/Qilin-0.9.7-SNAPSHOT.jar:/mnt/data/MyOwnFolder/learning/p_algo/logback-classic-1.3.0.jar driver.Main  -pae -pe -clinit=ONFLY -lcs -mh -pta=1c -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-core-2.19.2-sources.jar -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-annotations-3.0-rc5-sources.jar  -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-databind-2.19.2.jar -jre=/mnt/data/MyOwnFolder/learning/p_algo/Qilin/artifact/benchmarks/JREs/jre1.6.0_45 -dumppts && cp /mnt/data/MyOwnFolder/learning/p_algo/Qilin/sootOutput/pts.txt /mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs/result_qilin_jackson.txt
# cd "/mnt/data/MyOwnFolder/learning/p_algo/Qilin" && java -cp ./artifact/Qilin-0.9.7-SNAPSHOT.jar:/mnt/data/MyOwnFolder/learning/p_algo/logback-classic-1.3.0.jar driver.Main  -pae -pe -clinit=ONFLY -lcs -mh -pta=1c -apppath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-core-2.19.2-sources.jar -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-annotations-3.0-rc5-sources.jar  -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-databind-2.19.2.jar -jre=/mnt/data/MyOwnFolder/learning/p_algo/jdk8u462-b08 -dumppts && cp /mnt/data/MyOwnFolder/learning/p_algo/Qilin/sootOutput/pts.txt /mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs/result_qilin_jackson.txt
# cd "/mnt/data/MyOwnFolder/learning/p_algo/Qilin" && java -cp ./artifact/Qilin-0.9.7-SNAPSHOT.jar:/mnt/data/MyOwnFolder/learning/p_algo/logback-classic-1.3.0.jar driver.Main  -pae -pe -clinit=ONFLY -lcs -mh -pta=1c -apppath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-core-2.19.2-sources.jar -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-annotations-3.0-rc5-sources.jar  -libpath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson-databind-2.19.2.jar -jre=/mnt/data/MyOwnFolder/learning/p_algo/Qilin/artifact/benchmarks/JREs/jre1.8.0_121_debug -dumppts && cp /mnt/data/MyOwnFolder/learning/p_algo/Qilin/sootOutput/pts.txt /mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs/result_qilin_jackson.txt

# cd "/mnt/data/MyOwnFolder/learning/p_algo/Qilin" && java -cp ./artifact/Qilin-0.9.7-SNAPSHOT.jar:/mnt/data/MyOwnFolder/learning/p_algo/logback-classic-1.3.0.jar driver.Main  -pae -pe -clinit=ONFLY -lcs -mh -pta=1c -apppath /mnt/data/MyOwnFolder/learning/p_algo/jackson/jackson.jar -jre=/mnt/data/MyOwnFolder/learning/p_algo/jdk8u462-b08 -dumppts && cp /mnt/data/MyOwnFolder/learning/p_algo/Qilin/sootOutput/pts.txt /mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs/result_qilin_jackson.txt

# #EntrySize:10
# Time (sec):                                       39.0880012512207
# #Reachable Method (CI):                           12316
# #Call Edge(CI):                                   63312
# #May Fail Cast (Total):                           1124
# #Virtual Call Site(Polymorphic):                  1706
# #globalAlias_incstst:                             25925
# #Avg Points-to Target without Native Var(CI):     32.5375162799672

# Main PTA (including pre-analysis) elapsed time: 48,65s
# Main PTA consumed memory: 4183,20 MB

# cd "/mnt/data/MyOwnFolder/learning/p_algo/Qilin" && java -cp ./artifact/Qilin-0.9.7-SNAPSHOT.jar:/mnt/data/MyOwnFolder/learning/p_algo/logback-classic-1.3.0.jar driver.Main  -pae -pe -clinit=ONFLY -lcs -mh -pta=1c -apppath /mnt/data/MyOwnFolder/learning/p_algo/reactor-core/reactor-core.jar -jre=/mnt/data/MyOwnFolder/learning/p_algo/jdk8u462-b08 -dumppts && cp /mnt/data/MyOwnFolder/learning/p_algo/Qilin/sootOutput/pts.txt /mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs/result_qilin_reactor_core.txt
# k-callsite PTA ...
# include implicit entry!
# #EntrySize:11
# Time (sec):                                       39.36000061035156
# #Reachable Method (CI):                           12370
# #Call Edge(CI):                                   63563
# #May Fail Cast (Total):                           1125
# #Virtual Call Site(Polymorphic):                  1721
# #globalAlias_incstst:                             25977
# #Avg Points-to Target without Native Var(CI):     32.52088868584619

# Main PTA (including pre-analysis) elapsed time: 48,95s
# Main PTA consumed memory: 4289,73 MB

# cd "/mnt/data/MyOwnFolder/learning/p_algo/Qilin" && java -cp ./artifact/Qilin-0.9.7-SNAPSHOT.jar:/mnt/data/MyOwnFolder/learning/p_algo/logback-classic-1.3.0.jar driver.Main  -pae -pe -clinit=ONFLY -lcs -mh -pta=1c -apppath /mnt/data/MyOwnFolder/learning/p_algo/jackrabbit/jackrabbit.jar -jre=/mnt/data/MyOwnFolder/learning/p_algo/jdk8u462-b08 -dumppts && cp /mnt/data/MyOwnFolder/learning/p_algo/Qilin/sootOutput/pts.txt /mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs/result_qilin_jackrabbit.txt
# #EntrySize:11
# Time (sec):                                       41.30400085449219
# #Reachable Method (CI):                           12336
# #Call Edge(CI):                                   63382
# #May Fail Cast (Total):                           1125
# #Virtual Call Site(Polymorphic):                  1706
# #globalAlias_incstst:                             25927
# #Avg Points-to Target without Native Var(CI):     32.53066486733981

# Main PTA (including pre-analysis) elapsed time: 51,73s
# Main PTA consumed memory: 4256,81 MB

# cd "/mnt/data/MyOwnFolder/learning/p_algo/Qilin" && java -Xmx8g -cp ./artifact/Qilin-0.9.7-SNAPSHOT.jar:/mnt/data/MyOwnFolder/learning/p_algo/logback-classic-1.3.0.jar driver.Main  -pae -pe -clinit=ONFLY -lcs -mh -pta=1c -apppath /mnt/data/MyOwnFolder/learning/p_algo/Openfire/Openfire.jar -jre=/mnt/data/MyOwnFolder/learning/p_algo/jdk8u462-b08 -dumppts && cp /mnt/data/MyOwnFolder/learning/p_algo/Qilin/sootOutput/pts.txt /mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs/result_qilin_openfire.txt
# OuM
# 8Gb
# #EntrySize:11
# Time (sec):                                       116.40899658203125
# #Reachable Method (CI):                           28240
# #Call Edge(CI):                                   151176
# #May Fail Cast (Total):                           4013
# #Virtual Call Site(Polymorphic):                  6115
# #globalAlias_incstst:                             46907
# #Avg Points-to Target without Native Var(CI):     73.64788449227285

# Main PTA (including pre-analysis) elapsed time: 144,87s
# Main PTA consumed memory: 8775,52 MB

