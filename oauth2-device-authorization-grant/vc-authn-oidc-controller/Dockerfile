FROM mcr.microsoft.com/dotnet/core/sdk:3.1 AS build-env
WORKDIR /app

# Copy sln and csproj and restore as distinct layers
RUN git clone https://github.com/bcgov/vc-authn-oidc.git ./checkout
# COPY oidc-controller/src/*.sln ./
# COPY oidc-controller/src/*/*.csproj ./
# RUN for file in $(ls *.csproj); do mkdir -p ./${file%.*}/ && mv $file ./${file%.*}/; done
# RUN dotnet restore

# Copy everything else and build app
# COPY oidc-controller/src ./
RUN cp -a ./checkout/oidc-controller/src/* .
RUN ls -la
RUN for file in $(ls *.csproj); do mkdir -p ./${file%.*}/ && mv $file ./${file%.*}/; done
RUN dotnet restore
RUN ls -la
RUN dotnet publish -c Release -o /app/out --no-restore

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1

EXPOSE 5000

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client
COPY --from=build-env /app/out .
COPY import.sh ./
CMD ["dotnet", "VCAuthn.dll"]