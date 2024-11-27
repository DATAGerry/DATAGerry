import { Component, OnInit } from '@angular/core';
import { WebhookService } from '../../services/webhook.service';
import { WebhookLog } from '../../models/webhook.model';
import { ToastService } from 'src/app/layout/toast/toast.service';

@Component({
    selector: 'app-webhook-log-viewer',
    templateUrl: './webhook-log-viewer.component.html',
    styleUrls: ['./webhook-log-viewer.component.scss'],
})
export class WebhookLogViewerComponent implements OnInit {
    public logs: WebhookLog[] = [];
    public loading = false;
    public columns = [
        { display: 'Date', data: 'date' },
        { display: 'Status', data: 'status' },
        { display: 'Response Code', data: 'response_code' },
    ];

    constructor(private webhookService: WebhookService, private toast: ToastService) { }

    ngOnInit(): void {
        // this.loadLogs();
    }

    private loadLogs(): void {
        this.loading = true;
        this.webhookService.getWebhookLogs().subscribe({
            next: (data) => (this.logs = data),
            error: (err) => {
                this.toast.error(err?.error?.message)
                this.logs = [];
            },
            complete: () => (this.loading = false),
        });
    }
}
