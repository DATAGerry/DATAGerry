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
import { CmdbPort, PortCreatePayload } from '../models/ports-overview.types';
/* ------------------------------------------------------------------------------------------------------------------ */

/** Shape every insert route answers with: the new public_id plus the stored document. */
interface InsertSingleResponse<T> {
    result_id: number;
    raw: T;
}


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
    public createPort(payload: PortCreatePayload): Observable<CmdbPort> {
        const options = { headers: this.jsonHeaders, observe: resp };

        return this.api.callPost<InsertSingleResponse<CmdbPort>>(`${ this.servicePrefix }/`, payload, options).pipe(
            map((response: HttpResponse<InsertSingleResponse<CmdbPort>>) => response?.body?.raw)
        );
    }
}
