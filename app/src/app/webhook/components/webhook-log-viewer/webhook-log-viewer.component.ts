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
import { Component, OnInit } from '@angular/core';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { WebhookLogService } from '../../services/webhookLog.service';

@Component({
    selector: 'app-webhook-log-viewer',
    templateUrl: './webhook-log-viewer.component.html',
    styleUrls: ['./webhook-log-viewer.component.scss'],
})
export class WebhookLogViewerComponent implements OnInit {
    public logs: any[] = [];
    public loading = false;
    public datePlaceholder = 'YYYY-MM-DD';

    public columns = [
        { display: 'Webhook ID', name: 'webhook_id', data: 'webhook_id', searchable: true, sortable: true, style: { width: '30px', 'text-align': 'center' } },
        { display: 'Date', data: 'event_time', style: { 'text-align': 'center' } },
        { display: 'Status', data: 'status', style: { 'text-align': 'center' } },
        { display: 'Response Code', data: 'response_code', style: { width: '140px', 'text-align': 'center' } },
    ];

    constructor(
        private webhookService: WebhookLogService,
        private toast: ToastService) { }

    ngOnInit(): void {
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
}
