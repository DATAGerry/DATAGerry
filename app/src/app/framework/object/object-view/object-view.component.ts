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
import { ChangeDetectorRef, Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Data } from '@angular/router';

import { BehaviorSubject, Subject, takeUntil } from 'rxjs';

import { ObjectService } from '../../services/object.service';

import { CmdbMode } from '../../modes.enum';
import { RenderResult } from '../../models/cmdb-render';
import { ToastService } from 'src/app/layout/toast/toast.service';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-object-view',
    templateUrl: './object-view.component.html',
    styleUrls: ['./object-view.component.scss']
})
export class ObjectViewComponent implements OnInit, OnDestroy {

    public mode: CmdbMode = CmdbMode.View;
    public renderResult: RenderResult;
    private unsubscribe = new Subject();

    // Current type from the route resolve.
    private objectViewSubject: BehaviorSubject<RenderResult> = new BehaviorSubject<RenderResult>(undefined);

    /* --------------------------------------------------- LIFE CYLCE --------------------------------------------------- */
    constructor(public objectService: ObjectService, private activateRoute: ActivatedRoute, private changesRef: ChangeDetectorRef,
        private toastService: ToastService
    ) {
        this.activateRoute.data.subscribe((data: Data) => {
            this.objectViewSubject.next(data.object as RenderResult);
        },
            (e) => {
                this.toastService.error(e?.error?.message);
            });
    }


    public ngOnInit(): void {
        this.objectViewSubject.asObservable().pipe(takeUntil(this.unsubscribe))
            .subscribe((result) => {
                this.renderResult = result;
            },
                (e) => {
                    this.toastService.error(e?.error?.message);
                });
    }

    ngAfterViewInit(): void {
        this.changesRef.detectChanges();
    }


    public ngOnDestroy(): void {
        this.unsubscribe.complete();
    }

    /* ------------------------------------------------ HELPER FUNCTIONS ------------------------------------------------ */

    @HostListener('window:scroll')
    onWindowScroll() {
        const dialog = document.getElementsByClassName('object-view-navbar') as HTMLCollectionOf<any>;
        dialog[0].id = 'object-form-action';

        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            dialog[0].style.visibility = 'visible';
            dialog[0].classList.add('shadow');
        } else {
            dialog[0].classList.remove('shadow');
            dialog[0].id = '';
        }
    }
}
