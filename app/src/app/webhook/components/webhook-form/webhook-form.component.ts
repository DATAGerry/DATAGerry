import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { WebhookService } from '../../services/webhook.service';
import { Webhook } from '../../models/webhook.model';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { Location } from '@angular/common';

@Component({
    selector: 'app-webhook-form',
    templateUrl: './webhook-form.component.html',
    styleUrls: ['./webhook-form.component.scss'],
})
export class WebhookFormComponent implements OnInit {
    public webhookForm: FormGroup;
    publicId?: number;

    eventOptions = [
        { label: 'Create', value: 'CREATE' },
        { label: 'Update', value: 'UPDATE' },
        { label: 'Delete', value: 'DELETE' },
    ];

    /* --------------------------------------------------- LIFECYCLE METHODS -------------------------------------------------- */

    constructor(
        private fb: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private webhookService: WebhookService,
        private toast: ToastService,
        private location: Location
    ) {
        this.webhookForm = this.fb.group({
            name: ['', Validators.required],
            url: ['', [Validators.required, Validators.pattern(/^https?:\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/.*)?$/)]],
            event_types: [[], Validators.required],
            active: [true],
        });
    }


    ngOnInit(): void {
        this.publicId = this.route.snapshot.params['id'];
        if (this.publicId) {
            this.loadWebhookDetails(this.publicId);
        }
    }

    /* --------------------------------------------------- GETTERS -------------------------------------------------- */

    /**
     * Getter for the 'name' form control.
     * @returns The form control for the webhook's name field.
     */
    get name() {
        return this.webhookForm.get('name');
    }


    /**
     * Getter for the 'url' form control.
     * @returns The form control for the webhook's URL field.
     */
    get url() {
        return this.webhookForm.get('url');
    }


    /**
     * Getter for the 'event_types' form control.
     * @returns The form control for the webhook's event types field.
     */
    get eventTypes() {
        return this.webhookForm.get('event_types');
    }


    /* --------------------------------------------------- API CALLS -------------------------------------------------- */

    /**
     * Loads the details of a specific webhook by its public ID and updates the form with the retrieved data.
     * @param publicId - The public ID of the webhook to load.
     */
    private loadWebhookDetails(publicId: number): void {
        this.webhookService.getWebhookById(publicId).subscribe({
            next: (webhook) => {
                this.webhookForm.patchValue(webhook);
            },
            error: (err) => {
                this.toast.error(err?.error?.message)
            }
        });
    }


    /**
     * Saves the webhook by either creating a new webhook or updating an existing one based on the presence of a public ID.
     */
    public saveWebhook(): void {
        if (this.webhookForm.invalid) {
            this.toast.error('Please fill in all required fields with valid data.');
            return;
        }

        const webhook: Webhook = this.webhookForm.value;

        if (this.publicId) {
            // Update existing webhook
            this.webhookService.updateWebhook(this.publicId, webhook).subscribe({
                next: () => {
                    this.toast.success('Webhook updated successfully.');
                    this.router.navigate(['/webhooks']);
                },
                error: (err) => {
                    this.toast.error(err?.error?.message);
                },
            });
        } else {
            // Create new webhook
            this.webhookService.createWebhook(webhook).subscribe({
                next: () => {
                    this.toast.success('Webhook created successfully.');
                    this.router.navigate(['/webhooks']);
                },
                error: (err) => {
                    this.toast.error(err?.error?.message);
                }
            });
        }
    }

    /* --------------------------------------------------- ACTION METHODS -------------------------------------------------- */

    /**
     * Navigates back to the previous page in the browser's history.
     */
    goBack(): void {
        this.location.back()
    }
}