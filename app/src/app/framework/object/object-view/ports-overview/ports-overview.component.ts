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
import {
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
    Input,
    OnChanges,
    OnDestroy,
    SimpleChanges,
    inject
} from '@angular/core';

import { Observable, Subject, forkJoin, of } from 'rxjs';
import { catchError, finalize, map, switchMap, takeUntil } from 'rxjs/operators';

import { ExtendableOptionCatalogService } from 'src/app/core/services/extendable-option-catalog.service';
import { LoaderService } from 'src/app/core/services/loader.service';
import { PortOptionType } from 'src/app/framework/models/port-option-type';
import { Sort, SortDirection } from 'src/app/layout/table/table.types';
import { CmdbPort, PortRow } from './models/ports-overview.types';
import { PortService } from './services/port.service';
import {
    clampPage,
    hasConnectionState,
    hasPanelSides,
    pagePortRows,
    sortPortRows,
    toOptionLabels,
    toPortRows
} from './utils/ports-table.util';
/* ------------------------------------------------------------------------------------------------------------------ */

const DEFAULT_PAGE_SIZE = 10;

/** One load: the object's ports together with the option labels they are shown by. */
interface LoadedPorts {
    ports: CmdbPort[];
    labels: Map<string, string>;
}

/** The option lists the three select fields of a port draw their labels from. */
const PORT_OPTION_TYPES: readonly string[] = Object.values(PortOptionType);


/**
 * The ports section of an object view, shown in the attributes card like a multi-data section.
 *
 * The route hands over every port of the object in one answer, so sorting and paging are done here
 * rather than by the server.
 */
@Component({
    selector: 'cmdb-ports-overview',
    templateUrl: './ports-overview.component.html',
    styleUrls: ['./ports-overview.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    standalone: false
})
export class PortsOverviewComponent implements OnChanges, OnDestroy {

    private readonly portService = inject(PortService);
    private readonly optionCatalog = inject(ExtendableOptionCatalogService);
    private readonly loaderService = inject(LoaderService);
    private readonly changesRef = inject(ChangeDetectorRef);

    @Input() public objectId: number | null = null;

    /** The rows of the current page. */
    public rows: PortRow[] = [];

    /** What the pagination counts. */
    public totalRows = 0;

    public page = 1;
    public pageSize = DEFAULT_PAGE_SIZE;
    public sort: Sort = { name: 'port_number', order: SortDirection.ASCENDING };
    public showSideColumn = false;
    public showConnectionColumn = false;
    public hasError = false;
    public readonly isLoading$ = this.loaderService.isLoading$;

    private allRows: PortRow[] = [];

    private readonly destroy$ = new Subject<void>();
    private readonly load$ = new Subject<number>();

/* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */

    constructor() {
        // switchMap so a second object replaces a request still in flight instead of racing it.
        this.load$
            .pipe(
                switchMap((objectId) => this.readPorts(objectId)),
                takeUntil(this.destroy$)
            )
            .subscribe((loaded) => this.applyPorts(loaded));
    }

    public ngOnChanges(changes: SimpleChanges): void {
        if (changes['objectId']) {
            this.load();
        }
    }

    public ngOnDestroy(): void {
        this.destroy$.next();
        this.destroy$.complete();
    }

/* ---------------------------------------------------- EVENTS ------------------------------------------------------ */

    public onPageChange(page: number): void {
        this.page = page;
        this.applyQuery();
    }

    public onPageSizeChange(pageSize: number): void {
        this.pageSize = pageSize;
        this.page = 1;
        this.applyQuery();
    }

    public onSortChange(sort: Sort): void {
        this.sort = sort;
        this.page = 1;
        this.applyQuery();
    }

/* ------------------------------------------------ PRIVATE FUNCTIONS ----------------------------------------------- */

    private load(): void {
        if (this.objectId == null) {
            this.reset();
            return;
        }

        this.load$.next(this.objectId);
    }


    /**
     * The ports and the option lists their labels come from are read together, so the table is built
     * once instead of first showing ids and then replacing them.
     */
    private readPorts(objectId: number): Observable<LoadedPorts> {
        this.loaderService.show();
        this.hasError = false;

        return forkJoin({
            ports: this.portService.getPortsOfObject(objectId),
            options: this.optionCatalog.optionsForTypes(PORT_OPTION_TYPES)
        }).pipe(
            map(({ ports, options }) => ({ ports, labels: toOptionLabels(options) })),
            catchError(() => {
                this.hasError = true;
                return of<LoadedPorts>({ ports: [], labels: new Map() });
            }),
            finalize(() => {
                this.loaderService.hide();
                this.changesRef.markForCheck();
            })
        );
    }


    private applyPorts({ ports, labels }: LoadedPorts): void {
        this.allRows = toPortRows(ports, labels);
        this.showSideColumn = hasPanelSides(this.allRows);
        this.showConnectionColumn = hasConnectionState(ports);
        this.page = 1;
        this.applyQuery();
    }


    /** Recomputes the visible page from the full list. Nothing here talks to the server. */
    private applyQuery(): void {
        const ordered = sortPortRows(this.allRows, this.sort);

        this.totalRows = ordered.length;
        this.page = clampPage(this.page, this.totalRows, this.pageSize);
        this.rows = pagePortRows(ordered, this.page, this.pageSize);
        this.changesRef.markForCheck();
    }


    private reset(): void {
        this.allRows = [];
        this.rows = [];
        this.totalRows = 0;
        this.showSideColumn = false;
        this.showConnectionColumn = false;
        this.hasError = false;
        this.changesRef.markForCheck();
    }

}
