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

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { SupportedExporterExtension } from '../../../../export/export-objects/model/supported-exporter-extension';
import { RenderResult } from '../../../models/cmdb-render';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { ObjectService } from 'src/app/framework/services/object.service';
import { catchError, debounceTime, interval, Observable, of, Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'cmdb-object-table-head',
  templateUrl: './object-table-head.component.html',
  styleUrls: ['./object-table-head.component.scss']
})
export class ObjectTableHeadComponent implements OnInit, OnDestroy, OnChanges {

  @Input() public selectedObjects: Array<RenderResult> = [];
  @Input() public selectedObjectsIDs: Array<number> = [];
  @Input() public formatList: SupportedExporterExtension[] = [];
  @Input() public totalResults: number = 0;

  @Output() public fileExport: EventEmitter<any> = new EventEmitter<any>();
  @Output() public manyObjectDeletes: EventEmitter<any> = new EventEmitter<any>();

  @Input() public type: CmdbType;

  totalObjects: number = 100;
  usedObjects: number;
  usedObjects$: Observable<number>;

  private fetchTrigger$ = new Subject<void>();
  private destroy$ = new Subject<void>();

  isCloudModeEnabled = environment.cloudMode;

  public constructor(private router: Router, private objectService: ObjectService) { }

  ngOnInit(): void {
    this.fetchTrigger$.pipe(
      debounceTime(300),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.fetchUsedObjects();
    });

    this.fetchUsedObjects();
  }


  ngOnChanges(changes: SimpleChanges): void {
    const relevantChanges = ['selectedObjects', 'selectedObjectsIDs', 'type'];

    const hasRelevantChange = relevantChanges.some(prop => changes[prop]);

    if (hasRelevantChange) {
      this.fetchTrigger$.next();
    }
  }


  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    this.fetchTrigger$.complete();
  }



  /**
   * Fetch the count of used objects from the backend.
   */
  private fetchUsedObjects(): void {
    this.usedObjects$ = this.objectService.countObjects().pipe(
      catchError(error => {
        console.error('Error fetching used objects count:', error?.error?.message);
        return of(0);
      })
    );

    this.usedObjects$.subscribe(count => {
      this.usedObjects = count;
    });
  }


  /**
   * Determines the CSS class for a button based on the usage percentage of objects.
   * @returns A string representing the button's CSS class.
   */
  getButtonClass(): string {
    if (!this.isCloudModeEnabled) {
      return '';
    }

    // Prevent division by zero
    const percentage = this.totalObjects > 0 ? (this.usedObjects / this.totalObjects) * 100 : 0;

    if (percentage <= 50) {
      return 'btn-success';
    } else if (percentage <= 85) {
      return 'btn-warning';
    } else {
      return 'btn-danger';
    }
  }


  public onBulkChange(): void {
    this.router.navigate(['/framework/object/change/'],
      { state: { type: this.type, objects: this.selectedObjects } });
  }

  public exporter(see: SupportedExporterExtension, view: string = 'native'): void {
    see.view = view;
    this.fileExport.emit(see);
  }
}
