import {Component, OnDestroy, OnInit} from '@angular/core';
import { SystemService } from '../../../settings/system/system.service';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {Subscription} from 'rxjs';

@Component({
  selector: 'cmdb-feedback-form',
  templateUrl: './feedback-form.component.html',
  styleUrls: ['./feedback-form.component.scss']
})
export class FeedbackFormComponent implements OnInit, OnDestroy {

  public feedbackForm: FormGroup;
  public formListener: Subscription;
  public feedbackUrl: string = 'https://datagerry.com/feedback-v1/0/0/0/0/0/unknown/';

  constructor(private systemService: SystemService) {
    this.feedbackForm = new FormGroup({
      happiness: new FormControl(0),
      usability: new FormControl(0),
      functionality: new FormControl(0),
      performance: new FormControl(0),
      stability: new FormControl(0),
      version: new FormControl(''),
      email: new FormControl('', Validators.email),
    });
  }

  ngOnInit() {
    this.systemService.getDatagerryInformation().subscribe((infos: any) => {
      this.feedbackForm.get('version').setValue(infos.version);
    });

    this.formListener = this.feedbackForm.valueChanges.subscribe(value => {
      this.generateQRCode();
    });
  }

  generateQRCode() {
    let url = 'https://datagerry.com/feedback-v1/';
    url = url + this.feedbackForm.get('happiness').value.toString() + '/'
      + this.feedbackForm.get('usability').value.toString() + '/'
      + this.feedbackForm.get('functionality').value.toString() + '/'
      + this.feedbackForm.get('performance').value.toString() + '/'
      + this.feedbackForm.get('stability').value.toString() + '/'
      + this.feedbackForm.get('version').value.toString() + '/'
      + this.feedbackForm.get('email').value.toString();
    this.feedbackUrl = url;
  }

  ngOnDestroy() {
    this.formListener.unsubscribe();
  }
}
