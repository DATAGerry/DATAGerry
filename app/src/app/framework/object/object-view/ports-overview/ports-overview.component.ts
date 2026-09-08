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
    Type,
    inject
} from '@angular/core';

import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { Observable, Subject, forkJoin, of } from 'rxjs';
import { catchError, finalize, map, switchMap, takeUntil } from 'rxjs/operators';

import { DeleteModalService } from 'src/app/core/services/delete-modal.service';
import { ExtendableOptionCatalogService } from 'src/app/core/services/extendable-option-catalog.service';
import { FullscreenModalService } from 'src/app/core/services/fullscreen-modal.service';
import { LoaderService } from 'src/app/core/services/loader.service';
import { PermissionService } from 'src/app/modules/auth/services/permission.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { Sort, SortDirection } from 'src/app/layout/table/table.types';
import { PortCreateWizardModalComponent } from './components/port-create-wizard-modal/port-create-wizard-modal.component';
import { PortFormModalComponent } from './components/port-form-modal/port-form-modal.component';
import {
    CmdbPort,
    PORT_ADD_RIGHT,
    PORT_DELETE_RIGHT,
    PORT_EDIT_RIGHT,
    PORT_OPTION_TYPES,
    PortRow
} from './models/ports-overview.types';
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


/** The ports section of an object view. The route sends every port at once, so paging is client-side. */
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
    private readonly modalService = inject(NgbModal);
    private readonly fullscreenModal = inject(FullscreenModalService);
    private readonly deleteModal = inject(DeleteModalService);
    private readonly permission = inject(PermissionService);
    private readonly toastService = inject(ToastService);
    private readonly changesRef = inject(ChangeDetectorRef);

    @Input() public objectId: number | null = null;

    /** Ports are created from the object view; the edit form only lists them. */
    @Input() public manageable = false;

    /** Passed on as the modal's subtitle. */
    @Input() public objectLabel = '';

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
    public readonly portAddRight = PORT_ADD_RIGHT;

    private allRows: PortRow[] = [];

    /** The loaded ports by public_id, so an edit starts from the stored port and not from its row. */
    private portsById = new Map<number, CmdbPort>();

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
            // A different object starts at the front; a reload after a write keeps the page.
            this.page = 1;
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


    public onAddPort(): void {
        this.openForm(null);
    }


    /** The creation assistant: a whole device's ports, named and previewed server-side. */
    public onCreatePorts(): void {
        if (this.objectId == null) {
            return;
        }

        const modal = this.openModal(PortCreateWizardModalComponent);

        modal.componentInstance.objectId = this.objectId;
        modal.componentInstance.objectLabel = this.objectLabel;

        this.reloadWhenStored(modal);
    }


    public onEditPort(row: PortRow): void {
        const port = this.portsById.get(row.publicId);

        if (!port) {
            return;
        }

        this.openForm(port);
    }


    public onDeletePort(row: PortRow): void {
        this.deleteModal.confirmDelete({
            title: 'Delete port',
            itemType: 'Port',
            itemName: row.name,
            warningMessage: 'Any connection and interface link of this port is removed with it.',
            onConfirm: () => this.deletePort(row.publicId)
        });
    }

/* ---------------------------------------------------- FUNCTIONS --------------------------------------------------- */

    /** Both gate one action of the table and, together, its whole actions column. */
    public get canEdit(): boolean {
        return this.manageable && this.hasRight(PORT_EDIT_RIGHT);
    }


    public get canDelete(): boolean {
        return this.manageable && this.hasRight(PORT_DELETE_RIGHT);
    }

/* ------------------------------------------------ PRIVATE FUNCTIONS ----------------------------------------------- */

    private hasRight(right: string): boolean {
        return this.permission.hasRight(right) || this.permission.hasExtendedRight(right);
    }


    /** One modal for both writes; it reports `true` once the port is stored. */
    private openForm(port: CmdbPort | null): void {
        if (this.objectId == null) {
            return;
        }

        const modal = this.openModal(PortFormModalComponent);

        modal.componentInstance.objectId = this.objectId;
        modal.componentInstance.objectLabel = this.objectLabel;
        modal.componentInstance.port = port;

        this.reloadWhenStored(modal);
    }


    /** Hosted inside the fullscreen element while one is open; a body-level modal is not painted there. */
    private openModal<T>(component: Type<T>): NgbModalRef {
        return this.modalService.open(component, this.fullscreenModal.withFullscreenContainer({
            size: 'lg',
            windowClass: 'dg-modal-window',
            backdropClass: 'dg-modal-window-backdrop'
        }));
    }


    private reloadWhenStored(modal: NgbModalRef): void {
        // Dismissing rejects the promise; cancelling is not an error.
        modal.result.then(
            (stored: boolean) => {
                if (stored) {
                    this.load();
                }
            },
            () => undefined
        );
    }


    private deletePort(publicId: number): void {
        this.loaderService.show();

        this.portService.deletePort(publicId)
            .pipe(
                takeUntil(this.destroy$),
                finalize(() => this.loaderService.hide())
            )
            .subscribe({
                next: () => {
                    this.toastService.success('Port was successfully deleted!');
                    this.load();
                },
                error: (err) => this.toastService.error(err?.error?.message)
            });
    }


    private load(): void {
        if (this.objectId == null) {
            this.reset();
            return;
        }

        this.load$.next(this.objectId);
    }


    /** Ports and option labels are read together, so the table is built once instead of twice. */
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
        this.portsById = new Map(ports.map((port) => [port.public_id, port]));
        this.showSideColumn = hasPanelSides(this.allRows);
        this.showConnectionColumn = hasConnectionState(ports);
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
        this.portsById = new Map();
        this.rows = [];
        this.totalRows = 0;
        this.showSideColumn = false;
        this.showConnectionColumn = false;
        this.hasError = false;
        this.changesRef.markForCheck();
    }

}
