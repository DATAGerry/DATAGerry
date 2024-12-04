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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { WebhookLogService } from '../../services/webhookLog.service';
import { DeleteConfirmationModalComponent } from '../modal/delete-confirmation-modal.component';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'app-webhook-log-viewer',
    templateUrl: './webhook-log-viewer.component.html',
    styleUrls: ['./webhook-log-viewer.component.scss'],
})
export class WebhookLogViewerComponent implements OnInit {
    public logs: any[] = [];
    public loading = false;
    public datePlaceholder = 'YYYY-MM-DD';
    public columns: any[];

    @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;


    constructor(
        private webhookService: WebhookLogService,
        private toast: ToastService, private modalService: NgbModal,) { }

    ngOnInit(): void {
        this.columns = [
            { display: 'Webhook ID', name: 'webhook_id', data: 'webhook_id', searchable: true, sortable: true, style: { width: '30px', 'text-align': 'center' } },
            { display: 'Date', data: 'event_time', style: { 'text-align': 'center' } },
            { display: 'Status', data: 'status', style: { 'text-align': 'center' } },
            { display: 'Response Code', data: 'response_code', style: { width: '140px', 'text-align': 'center' } },
            { display: 'Actions', name: 'actions', template: this.actionsTemplate, sortable: false, style: { width: '80px', 'text-align': 'center' } }
        ];
        this.loadLogs();
    }


    /**
     * Loads logs by retrieving all webhooks and formatting the event time and status for each log.
     * Sets the loading state and handles errors gracefully.
     */
    private loadLogs(): void {
        this.loading = true;
        this.webhookService.getAllWebhooks().subscribe({
            next: (data) => {
                this.logs = data.results.map(log => ({
                    ...log,
                    event_time: this.formatEventDate(log.event_time),
                    status: log.status ? 'Active' : 'Inactive',
                }));
            },
            error: (err) => {
                this.toast.error(err?.error?.message);
                this.logs = [];
            },
            complete: () => (this.loading = false),
        });
    }


    /**
     * Formats the event time from a raw date object to a localized date string.
     * @param eventTime - The raw event time object to format.
     * @returns A formatted date string or a placeholder if the date is invalid.
     */
    private formatEventDate(eventTime: any): string {
        if (eventTime?.$date) {
            return new Date(eventTime.$date).toLocaleDateString('en-US');
        }
        return this.datePlaceholder;
    }


    /**
 * Initiates the deletion process for the specified webhook.
 * @param publicId - The public ID of the webhook to delete.
 */
    public deleteLog(publicId: number): void {
        this.webhookService.deleteWebhookLog(publicId).subscribe({
            next: (res) => {
                this.toast.success('Webhook deleted Sucessfully');
                this.loadLogs();
            },
            error: (err) => {
                this.toast.error(err?.error?.message)
            }
        })
    }

    /**
    * Opens the Delete Report modal and deletes the report if confirmed.
    * @param report - The report to delete.
    */
    public onDeleteLog(log: any): void {
        this.openDeleteModal(
            log,
            `Delete Log: ID: ${log.webhook_id}`,
            `Do you want to delete the log "${log.webhook_id}"? This action cannot be undone.`
        );
    }


    /**
     * Opens a delete confirmation modal for the specified item.
     * Passes the item details and a descriptive title to the modal, and deletes the item upon confirmation.
     * @param item - The item to be deleted.
     * @param title - The title to display in the modal.
     * @param description - The description to display in the modal (currently unused in the code).
     */
    public openDeleteModal(item: any, title: string, description: string): void {
        console.log('item', item)
        const modalRef = this.modalService.open(DeleteConfirmationModalComponent, { size: 'lg' });
        modalRef.componentInstance.title = title;
        modalRef.componentInstance.item = item;
        modalRef.componentInstance.itemType = 'log';
        modalRef.componentInstance.itemName = item.webhook_id;

        modalRef.result.then(
            (result) => {
                if (result === 'confirmed') {
                    this.deleteLog(item.public_id);
                }
            },
            () => { }
        );
    }
}
