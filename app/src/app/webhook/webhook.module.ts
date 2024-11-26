import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { TableModule } from "../layout/table/table.module";
import { WebhookFormComponent } from './components/webhook-form/webhook-form.component';
import { WebhookOverviewComponent } from './components/webhook-overview/webhook-overview.component';
import { WebhookLogViewerComponent } from './components/webhook-log-viewer/webhook-log-viewer.component';
import { NgSelectModule } from '@ng-select/ng-select';

const routes: Routes = [
    {
        path: '',
        data: {
            breadcrumb: 'Webhooks'
        },
        component: WebhookOverviewComponent
    },
    {
        path: 'create',
        data: {
            breadcrumb: 'Create WebHook'
        },
        component: WebhookFormComponent
    },
    {
        path: 'edit/:id',
        data: {
            breadcrumb: 'Edit WebHook'
        },
        component: WebhookFormComponent
    },
    {
        path: 'logs',
        data: {
            breadcrumb: 'WebHook Logs'
        },
        component: WebhookLogViewerComponent
    },
];

@NgModule({
    declarations: [
        WebhookOverviewComponent,
        WebhookFormComponent,
        WebhookLogViewerComponent,
    ],
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        RouterModule.forChild(routes),
        TableModule,
        NgSelectModule
    ],
    providers: [],
})
export class WebhookModule { }
