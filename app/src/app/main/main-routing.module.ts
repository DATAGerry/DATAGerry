import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../auth/guards/auth.guard';
import { MainComponent } from './main.component';
import { LAYOUT_COMPONENT_ROUTES } from '../layout/layout.module';


const routes: Routes = [
  {
    path: 'dashboard',
    data: {
      breadcrumb: 'Dashboard'
    },
    loadChildren: () => import('../dashboard/dashboard.module').then(m => m.DashboardModule)
  },
  {
    path: 'error',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Error'
    },
    loadChildren: () => import('../error/error.module').then(m => m.ErrorModule)
  },
  {
    path: 'search',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Search'
    },
    loadChildren: () => import('../search/search.module').then(m => m.SearchModule)
  },
  {
    path: 'framework',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Framework'
    },
    loadChildren: () => import('../framework/framework.module').then(m => m.FrameworkModule)
  },
  {
    path: 'import',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Import'
    },
    loadChildren: () => import('../import/import.module').then(m => m.ImportModule)
  },
  {
    path: 'export',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Export'
    },
    loadChildren: () => import('../export/export.module').then(m => m.ExportModule)
  },
  {
    path: 'management',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'User-Management'
    },
    loadChildren: () => import('../management/management.module').then(m => m.ManagementModule),
  },
  {
    path: 'settings',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Settings'
    },
    loadChildren: () => import('../settings/settings.module').then(m => m.SettingsModule)
  },
  {
    path: 'info',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Info'
    },
    loadChildren: () => import('../info/info.module').then(m => m.InfoModule)
  },
  {
    path: 'filemanager',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Filemanager'
    },
    loadChildren: () => import('../file-manager/file-manager.module').then(m => m.FileManagerModule)
  },
  {
    path: 'debug',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Debug'
    },
    loadChildren: () => import('../debug/debug.module').then(m => m.DebugModule)
  },
];

@NgModule({
  imports: [RouterModule.forChild(LAYOUT_COMPONENT_ROUTES), RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule {
}
