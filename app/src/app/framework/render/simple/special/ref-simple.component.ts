import { Component, OnInit } from '@angular/core';
import { RenderField } from '../../fields/components.fields';
import { RenderResult } from '../../../models/cmdb-render';
import { ObjectService } from '../../../services/object.service';

@Component({
  selector: 'cmdb-ref-simple',
  templateUrl: './ref-simple.component.html',
  styleUrls: ['./ref-simple.component.scss']
})
export class RefSimpleComponent extends RenderField implements OnInit {
  public refObject: RenderResult;

  constructor(private objectService: ObjectService) {
    super();
  }

  public ngOnInit(): void {
    if (this.data.value !== '' && this.data.value !== undefined && this.data.value !== null) {
      this.objectService.getObject(this.data.value).subscribe((refObject: RenderResult) => {
        this.refObject = refObject;
      });
    }
  }
}
