CREATE TABLE package (
    package_name  VARCHAR(100) PRIMARY KEY,
    launch_activity VARCHAR(150)
);

CREATE TABLE activity (
    activity_name VARCHAR(150),
    package_name  VARCHAR(100),
    FOREIGN KEY (package_name) REFERENCES package(package_name)
);

CREATE TABLE permissions (
    permission_name VARCHAR(100),
    package_name  VARCHAR(100),
    FOREIGN KEY (package_name) REFERENCES package(package_name)
);

