/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2026 becon GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Injectable, inject } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { ApiCallService, resp } from 'src/app/services/api-call.service';
import { APIInsertSingleResponse, APIUpdateSingleResponse } from 'src/app/services/models/api-response';
import { CmdbPort, PortPayload } from '../models/ports-overview.types';
/* ------------------------------------------------------------------------------------------------------------------ */

/** REST access to the ports of the CmdbObject collection `framework.ports`. */
@Injectable({ providedIn: 'root' })
export class PortService {

    public readonly servicePrefix = 'ports';

    private readonly api = inject(ApiCallService);
    private readonly jsonHeaders = new HttpHeaders({ 'Content-Type': 'application/json' });

/* ---------------------------------------------------- FUNCTIONS --------------------------------------------------- */

    /**
     * Every port of one object, already ordered by the backend (port number, then name).
     *
     * The route answers with a plain array, and an object without ports answers with an empty one -
     * "no ports yet" is a normal state, not an error.
     */
    public getPortsOfObject(objectId: number): Observable<CmdbPort[]> {
        const options = { headers: this.jsonHeaders, params: new HttpParams(), observe: resp };

        return this.api.callGet<CmdbPort[]>(`${ this.servicePrefix }/object/${ objectId }`, options).pipe(
            map((response: HttpResponse<CmdbPort[]>) => response?.body ?? [])
        );
    }


    /**
     * Creates one port and answers with the stored port.
     *
     * The owner rides in the payload: a port is created against an object, not under it. A name
     * already taken on that face of the object comes back as a readable 400.
     */
    public createPort(payload: PortPayload): Observable<CmdbPort> {
        const options = { headers: this.jsonHeaders, observe: resp };

        return this.api.callPost<APIInsertSingleResponse<CmdbPort>>(`${ this.servicePrefix }/`, payload, options).pipe(
            map((response: HttpResponse<APIInsertSingleResponse<CmdbPort>>) => response?.body?.raw)
        );
    }


    /**
     * Replaces one port with the payload and answers with its new data.
     *
     * The route takes the whole port, so every field has to be sent - an omitted one is stored as
     * null. Owner and side are immutable: naming a different one is refused, not ignored.
     */
    public updatePort(publicId: number, payload: PortPayload): Observable<CmdbPort> {
        const options = { headers: this.jsonHeaders, observe: resp };
        const route = `${ this.servicePrefix }/${ publicId }`;

        return this.api.callPut<APIUpdateSingleResponse<CmdbPort>>(route, payload, options).pipe(
            map((response: HttpResponse<APIUpdateSingleResponse<CmdbPort>>) => response?.body?.result)
        );
    }


    /** Deletes one port. Its connections and interface links go with it, server-side. */
    public deletePort(publicId: number): Observable<void> {
        const options = { headers: this.jsonHeaders, observe: resp };

        return this.api.callDelete<void>(`${ this.servicePrefix }/${ publicId }`, options).pipe(
            map(() => undefined)
        );
    }
}
