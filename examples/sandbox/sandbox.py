
from netpyne import specs, sim

import numpy

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters


## Population parameters
netParams.popParams['S'] = {'cellType': 'PYR', 'numCells': 10, 'cellModel': 'HH'}
netParams.popParams['M'] = {'cellType': 'PYR', 'numCells': 10, 'cellModel': 'HH'}


## Cell property rules
cellRule = {'conds': {'cellType': 'PYR'},  'secs': {}} 	# cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}  														# soma params dict
cellRule['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0}  									# soma geometry
cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}  		# soma hh mechanism
netParams.cellParams['PYRrule'] = cellRule  												# add dict to list of cell params

## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 5.0, 'e': 0}  # excitatory synaptic mechanism

# # Stimulation parameters
# netParams.stimSourceParams['bkg'] = {'type': 'VecStim', 'noise': 0.5, 'spkTimes': [20,50]}
# netParams.stimTargetParams['bkg->PYR'] = {'source': 'bkg', 'conds': {'cellType': 'PYR'}, 'weight': 0.1, 'delay': 5, 'synMech': 'exc'}

## Cell connectivity rules
netParams.connParams['S->M'] = { 	#  S -> M label
	'preConds': {'pop': 'S'}, 	# conditions of presyn cells
	'postConds': {'pop': 'M'}, # conditions of postsyn cells
	'probability': 1, 			# probability of connection
	'weight': 0.01, 				# synaptic weight
	'delay': 5,						# transmission delay (ms)
	'synMech': 'exc'}   			# synaptic mechanism


# Simulation options
simConfig = specs.SimConfig()		# object of class SimConfig to store simulation configuration

simConfig.duration = 0.5*1e3 			# Duration of the simulation, in ms
simConfig.dt = 0.025 				# Internal integration timestep to use
simConfig.verbose = False  			# Show detailed messages
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}  # Dict with traces to record
simConfig.recordStep = 0.1 			# Step size in ms to save data (eg. V traces, LFP, etc)
simConfig.filename = 'model_output'  # Set file output name
simConfig.savePickle = True 		# Save params, network and sim output to pickle file
simConfig.saveJson = False 	
simConfig.includeParamsLabel = False

simConfig.saveDataInclude = ['simData', 'simConfig', 'netParams']#, 'net']
simConfig.saveCellSecs = 1 #False
simConfig.saveCellConns = 1
# simConfig.recordLFP = [[150, y, 150] for y in [600, 800, 1000]] # only L5 (Zagha) [[150, y, 150] for y in range(200,1300,100)]

simConfig.analysis['plotRaster'] = True 			# Plot a raster
simConfig.analysis['plotTraces'] = {'include': [0]} 			# Plot recorded traces for this list of cells
#simConfig.analysis['plot2Dnet'] = True           # plot 2D visualization of cell positions and connections
#simConfig.analysis['plotLFP'] = True
#simConfig.printPopAvgRates =  [[250,500], [500,750], [750,1000]]



sim.create(netParams, simConfig)
#sim.net.cells[0].conns[0]['hObj'].event(100)
sim.simulate()
sim.analyze()
