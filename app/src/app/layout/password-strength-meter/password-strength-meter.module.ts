import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PasswordStrengthMeterComponent } from './password-strength-meter.component';

@NgModule({
  declarations: [PasswordStrengthMeterComponent],
  imports: [
    CommonModule
  ],
  exports: [PasswordStrengthMeterComponent]
})
export class PasswordStrengthMeterModule {
}
