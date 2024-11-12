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
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from '../auth/guards/auth.guard';

import { DashboardComponent } from '../../components/dashboard/dashboard.component';
/* ------------------------------------------------------------------------------------------------------------------ */

const routes: Routes = [
    {
        path: '',
        data: {
            breadcrumb: 'Dashboard'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        component: DashboardComponent
    },
    {
        path: 'error',
        data: {
            breadcrumb: 'Error'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../error/error.module').then(m => m.ErrorModule)
    },
    {
        path: 'search',
        data: {
            breadcrumb: 'Search'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../search/search.module').then(m => m.SearchModule)
    },
    {
        path: 'framework',
        data: {
            breadcrumb: 'Framework'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../../framework/framework.module').then(m => m.FrameworkModule)
    },
    {
        path: 'import',
        data: {
            breadcrumb: 'Import'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../import/import.module').then(m => m.ImportModule)
    },
    {
        path: 'export',
        data: {
            breadcrumb: 'Export'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../../export/export.module').then(m => m.ExportModule)
    },
    {
        path: 'management',
        data: {
            breadcrumb: 'User-Management'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../../management/management.module').then(m => m.ManagementModule),
    },
    {
        path: 'docapi',
        data: {
            breadcrumb: 'DocAPI'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../docapi/docapi.module').then(m => m.DocapiModule)
    },
    {
        path: 'settings',
        data: {
            breadcrumb: 'Settings'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../../settings/settings.module').then(m => m.SettingsModule)
    },
    {
        path: 'info',
        data: {
            breadcrumb: 'Info'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../info/info.module').then(m => m.InfoModule)
    },
    {
        path: 'filemanager',
        data: {
            breadcrumb: 'Filemanager'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../../filemanager/filemanager.module').then(m => m.FilemanagerModule)
    },
    {
        path: 'reports',
        data: {
            breadcrumb: 'Reports'
        },
        canActivate: [AuthGuard],
        canActivateChild: [AuthGuard],
        loadChildren: () => import('../../reporting/reporting.module').then(m => m.ReportingModule)
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class MainRoutingModule { }
