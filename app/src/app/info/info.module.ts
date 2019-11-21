import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { InfoRoutingModule } from './info-routing.module';
import { AboutComponent } from './components/about/about.component';
import { AboComponent } from './components/abo/abo.component';
import { ContactComponent } from './components/contact/contact.component';
import { TeamComponent } from './components/team/team.component';

@NgModule({
  declarations: [AboutComponent, AboComponent, ContactComponent, TeamComponent],
  imports: [
    CommonModule,
    InfoRoutingModule
  ]
})
export class InfoModule { }
