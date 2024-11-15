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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, OnInit, OnDestroy, TemplateRef, ViewChild } from '@angular/core';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ReportService } from 'src/app/reporting/services/report.service';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { APIGetMultiResponse } from 'src/app/services/models/api-response';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Sort, SortDirection } from 'src/app/layout/table/table.types';
import { AddCategoryModalComponent } from 'src/app/framework/category/components/modals/add-category-modal/add-category-modal.component';
import { DeleteConfirmationModalComponent } from '../../report-modal/delete-confirmation-modal.component';
import { ToastService } from 'src/app/layout/toast/toast.service';

@Component({
  selector: 'app-report-overview',
  templateUrl: './report-overview.component.html',
  styleUrls: ['./report-overview.component.scss']
})
export class ReportOverviewComponent implements OnInit, OnDestroy {
  private unsubscribe$ = new ReplaySubject<void>(1);
  public reports: Array<any> = [];
  public totalReports: number = 0;
  public limit: number = 10;
  public page: number = 1;
  public loading: boolean = false;
  public sort: Sort = { name: 'public_id', order: SortDirection.ASCENDING } as Sort;

  @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;

  public columns: Array<any>;

  /* --------------------------------------------------- LIFECYCLE METHODS -------------------------------------------------- */

  constructor(
    private reportService: ReportService,
    private modalService: NgbModal,
    private toast: ToastService
  ) { }


  ngOnInit(): void {
    this.columns = [
      { display: 'ID', name: 'public_id', data: 'public_id', sortable: true, style: { width: '80px', 'text-align': 'center' } },
      { display: 'Name', name: 'name', data: 'name', sortable: true, style: { width: 'auto', 'text-align': 'center' } },
      { display: 'Category', name: 'category', data: 'report_category_id', sortable: true, style: { width: '150px', 'text-align': 'center' } },
      { display: 'Actions', name: 'actions', template: this.actionsTemplate, sortable: false, style: { width: '150px', 'text-align': 'center' } }
    ];

    this.loadReports();
  }


  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /* --------------------------------------------------- API METHODS -------------------------------------------------- */

  /**
   * Loads reports based on the current pagination, sorting, and limit settings.
   * Updates the reports array and total reports count or logs an error if loading fails.
   */
  private loadReports(): void {
    this.loading = true;
    const params: CollectionParameters = {
      limit: this.limit,
      page: this.page,
      sort: this.sort.name,
      order: this.sort.order
    };

    this.reportService.getAllReports(params)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe({
        next: (response: APIGetMultiResponse<any>) => {
          if (response && response.results) {
            this.reports = response.results;
            this.totalReports = response.total || 0;
          } else {
            this.reports = [];
            this.totalReports = 0;
          }
          this.loading = false;
        },
        error: () => {
          this.reports = [];
          this.totalReports = 0;
          this.loading = false;
        }
      });
  }


  /* --------------------------------------------------- ACTIONS -------------------------------------------------- */

  /**
   * Runs the report with the specified ID.
   * @param id - The ID of the report to run.
   */
  public runReport(id: number): void {
    console.log('Run report with ID:', id);
    // Implement run report functionality
  }


  /**
   * Edits the report with the specified ID.
   * @param id - The ID of the report to edit.
   */
  public editReport(id: number): void {
    console.log('Edit report with ID:', id);
    // Implement edit report functionality
  }


  /**
   * Deletes the report with the specified public ID and reloads reports on success.
   * @param public_id - The public ID of the report to delete.
   */
  private deleteReport(public_id: number): void {
    this.reportService.deleteReport(public_id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe({
        next: () => {
          this.toast.success('Report deleted successfully');
          this.loadReports();
        },
        error: (error) => {
          this.toast.error(error?.error?.message);
        }
      });
  }



  /**
   * Handles pagination by updating the current page and reloading reports.
   * @param newPage - The new page number to load.
   */
  public onPageChange(newPage: number): void {
    this.page = newPage;
    this.loadReports();
  }

  /**
   * Updates the sort criteria and reloads the reports.
   * @param sort - The new sort criteria.
   */
  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.loadReports();
  }

  /* --------------------------------------------------- MODALS METHODS -------------------------------------------------- */


  /**
   * Opens the Add Report modal and reloads reports on successful addition.
   */
  public openAddReportModal(): void {
    const modalRef = this.modalService.open(AddCategoryModalComponent, { size: 'lg' });
    modalRef.result.then(
      (result) => {
        if (result === 'success') {
          this.loadReports();
        }
      },
      (error) => {
        this.toast.error(error?.error?.message)
      }
    );
  }

  /**
   * Opens the Delete Report modal and deletes the report if confirmed.
   * @param report - The report to delete.
   */
  public openDeleteReportModal(report: any): void {
    const modalRef = this.modalService.open(DeleteConfirmationModalComponent, { size: 'lg' });
    modalRef.componentInstance.report = report;
    modalRef.result.then(
      (result) => {
        if (result === 'confirmed') {
          this.deleteReport(report.public_id);
        }
      },
      () => { }
    );
  }
}