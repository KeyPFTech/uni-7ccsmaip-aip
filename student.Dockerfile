#Using the Planner image on my repo to get the base image
FROM adamfgreen/aip2020:latest
#Copy the input folder into the container and call it input e.g.
# ./input on your computer > /input on the container
COPY . /src
#Set the working directory to the input folder
WORKDIR /src

#Run the domain.pddl and problem.pddl in this folder on optic
# CMD optic domain.pddl problem.pddl


# tidybot https://github.com/potassco/pddl-instances/tree/master/ipc-2011/domains/tidybot-sequential-satisficing/instances
# visitall https://github.com/potassco/pddl-instances/tree/master/ipc-2011

# ADDITIVE heuristic
#CMD fd --overall-time-limit 1800s --overall-memory-limit 3500M ./tidybot-domain.pddl ./instances-optimal/tidybot-instance20.pddl --search "astar(add())";
#CMD fd --overall-time-limit 1800s --overall-memory-limit 3500M ./visitall-domain.pddl ./instances-optimal/visitall-instance20.pddl --search "astar(add())";

# MERGE AND SHRINK heuristic
#CMD fd --overall-time-limit 1800s --overall-memory-limit 3500M ./tidybot-domain.pddl ./instances-optimal/tidybot-instance20.pddl --search "astar(merge_and_shrink(merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance,dfp,total_order])),shrink_strategy=shrink_bisimulation(greedy=false)))";
CMD fd --overall-time-limit 1800s --overall-memory-limit 3500M ./visitall-domain.pddl ./instances-optimal/visitall-instance20.pddl --search "astar(merge_and_shrink(merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance,dfp,total_order])),shrink_strategy=shrink_bisimulation(greedy=false)))";


#Other software available is
# - fd
# - metricff
# - SMTPlan
# - Validate
# - enhsp
# Note all program names are case sensitive and as stated above
