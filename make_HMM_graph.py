import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

ax1 = plt.subplot(111)

G = nx.DiGraph()
G.add_node('x0', pos=(0,0))
G.add_node('xt-1', pos=(10,0))
G.add_node('xt', pos=(20,0))
G.add_node('y0', pos=(0,3))
G.add_node('yt-1', pos=(10,3))
G.add_node('yt', pos=(20,3))
G.add_node('z0', pos=(0,6))
G.add_node('zt-1', pos=(10,6))
G.add_node('zt', pos=(20,6))
G.add_node('label11', pos=(-10,0))
G.add_node('label12', pos=(-9,0))
G.add_node('label21', pos=(-10,3))
G.add_node('label22', pos=(-9,3))
G.add_node('label31', pos=(-10,6))
G.add_node('label32', pos=(-9,6))

G.add_edge('y0', 'x0')
G.add_edge('yt-1', 'xt-1')
G.add_edge('yt', 'xt')
G.add_edge('z0', 'y0')
G.add_edge('zt-1', 'yt-1')
G.add_edge('zt', 'yt')
G.add_edge('z0', 'zt-1')
G.add_edge('zt-1', 'zt')
G.add_edge('label11', 'label12', weight='Tweets')
G.add_edge('label21', 'label22', weight='Predicted Sentiment')
G.add_edge('label31', 'label32', weight='Actual Sentiment')
edge_labels = nx.get_edge_attributes(G,'weight')

node_labels = {}
node_labels['x0'] = 'x(0)'
node_labels['xt-1'] = 'x(t-1)'
node_labels['xt'] = 'x(t)'
node_labels['y0'] = 'y0'
node_labels['yt-1'] = 'y(t-1)'
node_labels['yt'] = 'y(t)'
node_labels['z0'] = 'z0'
node_labels['zt-1'] = 'z(t-1)'
node_labels['zt'] = 'z(t)'

pos=nx.get_node_attributes(G, 'pos')

nx.draw_networkx_nodes(G, pos, nodelist=['x0', 'xt-1', 'xt'], node_color='lightgray', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist=['y0', 'yt-1', 'yt'], node_color='lightskyblue', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist=['z0', 'zt-1', 'zt'], node_color='blue', node_size=3000)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

nx.draw_networkx_labels(G, pos, node_labels, font_size=12)

plt.axis('off')
plt.show()
