import { Component, AfterViewChecked } from '@angular/core';
import { RenderField } from '../../fields/components.fields';
import { RenderResult } from '../../../models/cmdb-render';
import { ObjectService } from '../../../services/object.service';

@Component({
  selector: 'cmdb-ref-simple',
  templateUrl: './ref-simple.component.html',
  styleUrls: ['./ref-simple.component.scss']
})
export class RefSimpleComponent extends RenderField implements AfterViewChecked {

  private dataValue: any = undefined;
  public refObject: any;

  constructor(private objectService: ObjectService) {
    super();
  }

  public ngAfterViewChecked() {
    if ( this.dataValue !== this.data.value) {
      this.dataValue  = parseInt(this.data.value, 10);
      if (this.dataValue) {
        this.objectService.getObject(this.data.value).subscribe((res: RenderResult) => {
          this.refObject = res;
        });
      } else { this.refObject = null; }
    }
  }
}
