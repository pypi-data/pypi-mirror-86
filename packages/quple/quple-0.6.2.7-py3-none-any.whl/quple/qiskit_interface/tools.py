import numpy as np
from qiskit.circuit import ParameterVector
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit import ParameterVector
from qiskit.aqua.algorithms.classifiers import QSVM 
from qiskit.aqua.components.feature_maps import FeatureMap
import quple
from quple.utils.utils import parallel_run
from qiskit.tools import parallel_map

def get_qiskit_state_vectors_test(quantum_instance, feature_map, x):
    is_statevector_sim = quantum_instance.is_statevector

    measurement = not is_statevector_sim
    measurement_basis = '0' * feature_map.num_qubits

        
    # build parameterized circuits, it could be slower for building circuit
    # but overall it should be faster since it only transpile one circuit
    feature_map_params = ParameterVector('x', feature_map.feature_dimension)
    parameterized_circuit = QSVM._construct_circuit(
        (feature_map_params, feature_map_params), feature_map, measurement,
        is_statevector_sim=is_statevector_sim)
    parameterized_circuit = quantum_instance.transpile(parameterized_circuit)[0]
    circuits = [parameterized_circuit.assign_parameters({feature_map_params: params})
                for params in x]        
    results = quantum_instance.execute(circuits, had_transpiled=True) 
    statevectors = np.array([results.get_statevector(i) for i in range(len(results.results))])
    return statevectors


def get_qiskit_state_vectors(quantum_instance, feature_map, x):
    if not quantum_instance.is_statevector:
        raise ValueError('Quantum instance must be a statevector simulator')
    q = QuantumRegister(feature_map.num_qubits, 'q')
    c = ClassicalRegister(feature_map.num_qubits, 'c')
    qc = QuantumCircuit(q, c)
    
    
    if isinstance(feature_map, QuantumCircuit):
                use_parameterized_circuits = True
    else:
        use_parameterized_circuits = feature_map.support_parameterized_circuit    
    if isinstance(feature_map, FeatureMap):
      data_pair = [(d, d) for d in x]
      circuits = parallel_map(QSVM._construct_circuit,
                              data_pair,
                              task_args=(feature_map, False, True),
                              num_processes=quple.MAX_WORKERS)
    else:
      feature_map_params = ParameterVector('x', feature_map.feature_dimension)
      parameterized_circuit = QSVM._construct_circuit(
          (feature_map_params, feature_map_params), feature_map, False,
          is_statevector_sim=True)
      parameterized_circuit = quantum_instance.transpile(parameterized_circuit)[0]
      circuits = [parameterized_circuit.assign_parameters({feature_map_params: params})
                  for params in x]     
    results = quantum_instance.execute(circuits, had_transpiled=use_parameterized_circuits) 
    statevectors = np.array([results.get_statevector(i) for i in range(len(results.results))])
    return statevectors
    
    
'''
    def construct_circuit(data):
        return feature_map.construct_circuit(data, q)
    circuits = parallel_run(construct_circuit, x)
    
'''    
