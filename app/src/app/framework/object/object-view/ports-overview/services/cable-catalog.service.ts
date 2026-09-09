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

import { Observable, forkJoin, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { ExtendableOptionCatalogService } from 'src/app/core/services/extendable-option-catalog.service';
import { CableOptionType } from 'src/app/framework/models/cable-option-type';
import { FieldOption } from 'src/app/framework/models/cmdb-section-template';
import { CmdbType } from 'src/app/framework/models/cmdb-type';
import { SpecialType } from 'src/app/framework/models/special-type';
import { TypeService } from 'src/app/framework/services/type.service';

import { CABLE_OPTION_TYPES } from '../models/port-connection.types';
/* ------------------------------------------------------------------------------------------------------------------ */

/** What the cable step of the connection wizard needs before it can be filled in. */
export interface CableCatalog {
    cableTypeOptions: FieldOption[];

    /** Types carrying the CABLE marker; only their objects can be an inventoried cable. */
    cableCiTypeIds: number[];
}


/** The two lookups a cable is described from, read together. */
@Injectable({ providedIn: 'root' })
export class CableCatalogService {

    private readonly optionCatalog = inject(ExtendableOptionCatalogService);
    private readonly typeService = inject(TypeService);

/* ---------------------------------------------------- FUNCTIONS --------------------------------------------------- */

    public read(): Observable<CableCatalog> {
        return forkJoin({
            cableTypeOptions: this.readCableTypeOptions(),
            cableCiTypeIds: this.readCableCiTypes()
        });
    }

/* ------------------------------------------------ PRIVATE FUNCTIONS ----------------------------------------------- */

    private readCableTypeOptions(): Observable<FieldOption[]> {
        return this.optionCatalog.optionsForTypes(CABLE_OPTION_TYPES).pipe(
            map((optionsByType) => optionsByType.get(CableOptionType.CABLE_TYPE) ?? [])
        );
    }


    /**
     * The types a cable CI may have.
     *
     * An empty answer is a configuration state rather than an error - no type carries the Cable marker
     * yet - and the caller says so instead of failing.
     */
    private readCableCiTypes(): Observable<number[]> {
        return this.typeService
            .getTypes({ filter: { special_type: SpecialType.CABLE }, limit: 0, sort: 'public_id', order: 1, page: 1 })
            .pipe(
                map((response) => ((response?.results ?? []) as CmdbType[]).map((type) => type.public_id)),
                catchError(() => of<number[]>([]))
            );
    }
}
