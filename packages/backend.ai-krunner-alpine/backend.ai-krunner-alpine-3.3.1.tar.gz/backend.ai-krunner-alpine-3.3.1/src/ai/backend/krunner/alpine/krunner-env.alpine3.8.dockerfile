FROM lablup/backendai-krunner-python:alpine3.8

ARG PREFIX=/opt/backend.ai

# for installing source-distributed Python packages, we need build-base.
# (we cannot just run manylinux wheels in Alpine due to musl-libc)
RUN apk add --no-cache build-base xz linux-headers
RUN ${PREFIX}/bin/pip install --no-cache-dir -U pip setuptools

COPY requirements.txt /root/
RUN ${PREFIX}/bin/pip install --no-cache-dir -U -r /root/requirements.txt && \
    ${PREFIX}/bin/pip list

# Create directories to be used for additional bind-mounts by the agent
RUN PYVER_MM="$(echo $PYTHON_VERSION | cut -d. -f1).$(echo $PYTHON_VERSION | cut -d. -f2)" && \
    mkdir -p ${PREFIX}/lib/python${PYVER_MM}/site-packages/ai/backend/kernel && \
    mkdir -p ${PREFIX}/lib/python${PYVER_MM}/site-packages/ai/backend/helpers

COPY ttyd_linux.x86_64.bin ${PREFIX}/bin/ttyd
COPY licenses/* ${PREFIX}/licenses/wheels/
RUN chmod +x ${PREFIX}/bin/ttyd

# Build the image archive
RUN cd ${PREFIX}; \
    tar cJf /root/image.tar.xz ./*

LABEL ai.backend.krunner.version=6
CMD ["${PREFIX}/bin/python"]

# vim: ft=dockerfile
