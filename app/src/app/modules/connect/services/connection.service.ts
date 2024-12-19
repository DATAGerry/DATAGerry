/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.
*
* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/


import { Injectable } from "@angular/core";
import { HttpBackend, HttpClient } from "@angular/common/http";

import { BehaviorSubject, Observable, lastValueFrom } from "rxjs";
import { environment } from "../../../../environments/environment";
/* ------------------------------------------------------------------------------------------------------------------ */

@Injectable({
    providedIn: "root",
})
export class ConnectionService {

    private connectionSubject: BehaviorSubject<string>;
    public connection: Observable<string>;
    private connectionStatus: boolean = false;
    private http: HttpClient;

    /* -------------------------------------------------- GETTER/SETTER ------------------------------------------------- */

    public get status(): boolean {
        return this.connectionStatus;
    }

    public get currentConnection(): any {
        return this.connectionSubject.value;
    }

    /* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */

    public constructor(private backend: HttpBackend) {
        this.http = new HttpClient(backend);
        this.connectionSubject = new BehaviorSubject<string>(
            JSON.parse(localStorage.getItem("connection"))
        );
        this.connection = this.connectionSubject.asObservable();

        if (this.currentConnection === null) {
            this.setDefaultConnection();
        }

        try {
            const connectionStatusPromise = this.connect();
            connectionStatusPromise.then((status) => {
                this.connectionStatus = status;

                if (this.connectionStatus === false) {
                    localStorage.removeItem("connection");
                    this.connectionSubject.next(null);
                }
            });
        } catch (e) {
            this.connectionStatus = false;
            localStorage.removeItem("connection");
            this.connectionSubject.next(null);
        }
    }

    /* ---------------------------------------------------- FUNCTIONS --------------------------------------------------- */

    /**
     * Sets the default connection URL using environment variables for protocol, host, and port.
     */
    private setDefaultConnection() {
        this.setConnectionURL(environment.protocol, environment.apiUrl, environment.apiPort);
    }


    /**
     * Tests the current connection by attempting to connect to the backend.
     * @returns A promise resolving to `true` if the connection is successful, otherwise `false`.
     */
    public async testConnection() {
        try {
            await this.connect();
            return true;
        } catch (e) {
            return false;
        }
    }


    /**
     * Attempts to connect to the backend using the current connection URL.
     * Logs the connection attempt and resolves the HTTP response.
     * @returns A promise resolving to the backend's connection response.
     */
    private async connect() {
        // console.log(
        //     `### CONNECTION TRY with URL: ${this.currentConnection}/rest/ ###`
        // );
        const conn_result$ = this.http.get<any>(
            `${this.currentConnection}/rest/`
        );

        return await lastValueFrom(conn_result$);
    }


    /**
     * Tests a custom backend URL by constructing it from the provided protocol, host, and port.
     * Logs the connection attempt and resolves the HTTP response.
     * @param protocol - The protocol to use (e.g., 'http', 'https').
     * @param host - The host address of the backend.
     * @param port - The port number of the backend.
     * @returns A promise resolving to the backend's connection response.
     */
    public async testCustomURL(protocol: string, host: string, port: number) {
        const customURL = `${protocol}://${host}:${port}/rest/`;
        // console.log(`Trying to connect to backend @ ${customURL}`);
        const conn_test_result$ = this.http.get<any>(customURL);

        return await lastValueFrom(conn_test_result$);
    }


    /**
     * Sets the connection URL based on the provided protocol, host, and port.
     * Updates the local storage and notifies subscribers of the new connection URL.
     * @param protocol - The protocol to use (e.g., 'http', 'https').
     * @param host - The host address of the backend.
     * @param port - The port number of the backend.
     */
    public setConnectionURL(protocol: string, host: string, port: number) {

        // Remove any existing protocol from the host
        host = host.replace(/^https?:\/\//, '');
        let href = "";

        if (port === 0) {
            href = `${protocol}://${host}`;
        } else {
            href = `${protocol}://${host}:${port}`;
        }

        localStorage.setItem("connection", JSON.stringify(href));
        this.connectionSubject.next(href);
    }
}