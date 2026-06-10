

# visNetwork
# http://dataknowledge.github.io/visNetwork


library(visNetwork)
nodes <- data.frame(id = 1:6, title = paste("node", 1:6), 
                    shape = c("dot", "square"),
                    size = 10:15, color = c("blue", "red"))
edges <- data.frame(from = 1:5, to = c(5, 4, 6, 3, 3))
visNetwork(nodes, edges) |>
  visOptions(highlightNearest = TRUE, nodesIdSelection = TRUE)