FROM taktile/base-serving-api-arrow:__version__
ENV APPDIR /app

# Install requirements
COPY ./requirements.txt ${APPDIR}/user_requirements.txt
RUN pip install -r ${APPDIR}/user_requirements.txt

# Copy code and assets for running the application
COPY ./src ${APPDIR}/src
COPY ./assets ${APPDIR}/assets
COPY ./tests ${APPDIR}/user_tests
COPY ./scripts ${APPDIR}/scripts

ARG RESOURCE_NAME
ARG DEPLOYMENT_API_URI
ARG COMMIT_HASH
ARG LOCAL_CLUSTER
ARG TAKTILE_UPDATE_KEY

# Run tests conditionally
RUN /app/scripts/tests-run.sh $RESOURCE_NAME && \
    python -m scripts.export_tests --commit-hash $COMMIT_HASH \
                                   --token $TAKTILE_UPDATE_KEY \
                                   --url $DEPLOYMENT_API_URL \
                                   --resource-name $RESOURCE_NAME \
                                   --local-cluster $LOCAL_CLUSTER


