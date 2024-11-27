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
import { Injectable } from '@angular/core';
import { HttpBackend, HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, lastValueFrom, of } from 'rxjs';
import { environment } from 'src/environments/environment';
import { ToastService } from 'src/app/layout/toast/toast.service';
@Injectable({
    providedIn: 'root'
})
export class ConnectionService {

    private readonly apiUrl: string;
    private connectionSubject: BehaviorSubject<string>;
    public connection: Observable<string>;
    private connectionStatus: boolean = false;
    private http: HttpClient;

    /* -------------------------------------------------- GETTER/SETTER ------------------------------------------------- */

    public get status(): boolean {
        return this.connectionStatus;
    }

    public get currentConnection(): string | null {
        return this.connectionSubject.value;
    }

    /* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */

    public constructor(private backend: HttpBackend, private toast: ToastService) {
        this.http = new HttpClient(backend);
        this.apiUrl = environment.apiUrl;

        // Initialize connectionSubject with null to trigger setDefaultConnection
        this.connectionSubject = new BehaviorSubject<string | null>(null);
        this.connection = this.connectionSubject.asObservable();

        // Set default connection from environment
        this.setDefaultConnection();

        // Attempt to connect using the default API URL
        this.connect().then(status => {
            this.connectionStatus = status;

            if (!this.connectionStatus) {
                this.connectionSubject.next(null);
                this.toast.error('Initial connection failed. API URL has been reset to null.')
            }
        }).catch((error) => {
            this.connectionStatus = false;
            this.connectionSubject.next(null);
            console.error(error);
            this.toast.error(error?.error?.message)

        });
    }

    /* ---------------------------------------------------- FUNCTIONS --------------------------------------------------- */

    /**
     * Sets the default connection URL from the environment configuration.
     */
    private setDefaultConnection(): void {
        try {
            this.connectionSubject.next(this.apiUrl);
            console.log(`Default API URL set to: ${this.apiUrl}`);
        } catch (error) {
            this.toast.error(error?.error?.message)
        }
    }

    /**
     * Attempts to connect to the API endpoint.
     * @returns Promise<boolean> indicating connection success.
     */
    public async testConnection(): Promise<boolean> {
        try {
            await this.connect();
            console.log('Test connection successful.');
            return true;
        } catch (error) {
            this.toast.error(error?.error?.message)
            return false;
        }
    }

    /**
     * Connects to the API endpoint to verify its availability.
     * @returns Promise<boolean> indicating connection success.
     */
    private async connect(): Promise<boolean> {
        if (!this.currentConnection) {
            this.toast.error('No API URL is set. Cannot attempt connection.')
            return false;
        }

        console.log(`### CONNECTION TRY with URL: ${this.currentConnection}/rest/ ###`);
        try {
            await lastValueFrom(this.http.get<any>(`${this.currentConnection}/rest/`));
            console.log('Connection successful.');
            return true;
        } catch (error) {
            console.error(`Connection attempt to ${this.currentConnection}/rest/ failed:`, error);
            this.toast.error(error?.error?.message)
            return false;
        }
    }

    /**
     * Tests a custom API URL provided by the user.
     * @param protocol The protocol to use (e.g., 'http', 'https').
     * @param host The host address.
     * @param port The port number.
     * @returns Promise<boolean> indicating if the custom URL is reachable.
     */
    public async testCustomURL(protocol: string, host: string, port: number): Promise<boolean> {
        const customURL = `${protocol}://${host}:${port}/rest/`;
        console.log(`Trying to connect to backend @ ${customURL}`);
        try {
            await lastValueFrom(this.http.get<any>(customURL));
            console.log(`Custom URL connection successful: ${customURL}`);
            return true;
        } catch (error) {
            console.error(`Custom URL test failed for ${customURL}:`, error);
            return false;
        }
    }

    /**
     * Sets a new connection URL based on provided protocol, host, and port.
     * @param protocol The protocol to use (e.g., 'http', 'https').
     * @param host The host address.
     * @param port The port number.
     */
    public setConnectionURL(protocol: string, host: string, port: number): void {
        let href = '';

        if (port === 0) {
            href = `${protocol}://${host}`;
        } else {
            href = `${protocol}://${host}:${port}`;
        }

        try {
            this.connectionSubject.next(href);
            console.log(`Connection URL updated to: ${href}`);
        } catch (error) {
            this.toast.error(error?.error?.message)
        }
    }
}