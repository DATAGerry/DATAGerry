import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConnectionComponent } from './connection.component';
import { ConnectionService } from './services/connection.service';
import { ConnectionGuard } from './guards/connection.guard';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [ConnectionComponent],
  imports: [
    CommonModule,
    FormsModule
  ],

  providers: [ConnectionService]
})
export class ConnectionModule {
}
