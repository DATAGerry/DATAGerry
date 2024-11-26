import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { WebhookService } from '../../services/webhook.service';
import { Webhook } from '../../models/webhook.model';
import { Router } from '@angular/router';
import { ToastService } from 'src/app/layout/toast/toast.service';

@Component({
    selector: 'app-webhook-overview',
    templateUrl: './webhook-overview.component.html',
    styleUrls: ['./webhook-overview.component.scss'],
})
export class WebhookOverviewComponent implements OnInit {
    public webhooks: Webhook[] = [];
    public totalWebhooks: number = 0;
    public page: number = 1;
    public limit: number = 10;
    public loading = false;

    @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>; // Reference the actions template
    @ViewChild('statusTemplate', { static: true }) statusTemplate: TemplateRef<any>; // Reference the template


    public columns: Array<any>;

    /* --------------------------------------------------- LIFECYCLE METHODS -------------------------------------------------- */

    constructor(private webhookService: WebhookService, private router: Router, private toast: ToastService) { }

    ngOnInit(): void {
        this.columns = [
            { display: 'ID', name: 'public_id_str', data: 'public_id', searchable: true, sortable: true, style: { width: '80px', 'text-align': 'center' } },
            { display: 'Name', name: 'name', data: 'name', sortable: true },
            { display: 'URL', name: 'url', data: 'url', sortable: true },
            { display: 'Actions', name: 'actions', template: this.actionsTemplate, sortable: false, style: { width: '80px', 'text-align': 'center' } },
        ];

        this.loadWebhooks();
    }

    /* --------------------------------------------------- API METHODS -------------------------------------------------- */

    /**
     * Loads all webhooks with the current pagination settings.
     * Sets the loading state, retrieves webhooks from the service, and updates component state.
     */
    private loadWebhooks(): void {
        this.loading = true;

        this.webhookService.getAllWebhooks({
            filter: '',
            limit: this.limit,
            page: this.page,
            sort: 'name',
            order: 1,
        }).subscribe({
            next: (data) => {
                this.webhooks = data.results;
                this.totalWebhooks = data.total;
                console.log('webhooks', this.webhooks)
            },
            error: (error) => {
                this.webhooks = [];
                this.totalWebhooks = 0;
                this.toast.error(error?.error?.message)
            },
            complete: () => (this.loading = false),
        });
    }

    /* --------------------------------------------------- ACTIONS -------------------------------------------------- */


    /**
     * Navigates to the edit page for the specified webhook.
     * @param publicId - The public ID of the webhook to edit.
     */
    public editWebhook(publicId: number): void {
        this.router.navigate([`/webhooks/edit`, publicId]);
    }


    /**
     * Initiates the deletion process for the specified webhook.
     * @param publicId - The public ID of the webhook to delete.
     */
    public deleteWebhook(publicId: number): void {
        console.log('Delete webhook:', publicId);
    }


    /**
     * Handles the page change event for pagination and reloads webhooks.
     * @param newPage - The new page number to load.
     */
    public onPageChange(newPage: number): void {
        this.page = newPage;
        this.loadWebhooks();
    }


    /**
     * Handles the change in page size, resets to the first page, and reloads webhooks.
     * @param newLimit - The new number of items per page.
     */
    public onPageSizeChange(newLimit: number): void {
        this.limit = newLimit;
        this.page = 1;
        this.loadWebhooks();
    }
}
