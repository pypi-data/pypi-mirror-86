After installing MemCNN run:

.. code:: bash

    python -m memcnn.train [MODEL] [DATASET] [--fresh] [--no-cuda]

* Available values for ``DATASET`` are ``cifar10`` and ``cifar100``.
* Available values for ``MODEL`` are ``resnet32``, ``resnet110``, ``resnet164``, ``revnet38``, ``revnet110``, ``revnet164``
* Use the ``--fresh`` flag to remove earlier experiment results.
* Use the ``--no-cuda`` flag to train on the CPU rather than the GPU through CUDA.

Datasets are automatically downloaded if they are not available.

When using Python 3.* replace the ``python`` directive with the appropriate Python 3 directive. For example when using the MemCNN docker image use ``python3.7``.
