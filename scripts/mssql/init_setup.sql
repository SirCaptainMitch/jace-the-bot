USE master;

/* In order to use this you must ensure that there is a server set up. */

/* Allow advanced options to be changed */
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
GO

/* Enable remote access */
EXEC sp_configure 'remote access', 1;
RECONFIGURE;
GO


/* Create a new login for the app user. */
CREATE LOGIN JaceApp
    WITH PASSWORD = '!ChangeMe!',
         CHECK_POLICY = OFF,
         CHECK_EXPIRATION = OFF;
GO


/* Setup and configure the app database */

DROP DATABASE IF EXISTS Jace;
GO

CREATE DATABASE Jace;
GO

USE Jace;
GO

/* Create a new database user associated with the login */
CREATE USER JaceApp FOR LOGIN JaceApp;
GO

/* Add the new user to the db_owner role (database administrator privileges) */
EXEC sp_addrolemember 'db_owner', 'JaceApp';
GO

