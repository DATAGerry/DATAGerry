import { Component, Input, OnInit } from '@angular/core';
import { ToastService } from '../../../../../layout/toast/toast.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { RenderResult } from '../../../../models/cmdb-render';

@Component({
  templateUrl: './object-link-add-modal.component.html',
  styleUrls: ['./object-link-add-modal.component.scss']
})
export class ObjectLinkAddModalComponent implements OnInit {

  // Object data
  @Input() renderResult: RenderResult = undefined;

  // Form
  public addLinkForm: FormGroup;

  constructor(private toast: ToastService, public activeModal: NgbActiveModal) {
    this.addLinkForm = new FormGroup({
      primary: new FormControl(null),
      secondary: new FormControl('', Validators.required)
    });
  }

  public ngOnInit(): void {

  }

}
