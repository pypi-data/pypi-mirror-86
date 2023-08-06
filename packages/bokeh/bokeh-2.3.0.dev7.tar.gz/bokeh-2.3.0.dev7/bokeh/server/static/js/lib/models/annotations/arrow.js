import { Annotation, AnnotationView } from "./annotation";
import { ArrowHead, OpenHead } from "./arrow_head";
import { ColumnarDataSource } from "../sources/columnar_data_source";
import { ColumnDataSource } from "../sources/column_data_source";
import { LineVector } from "../../core/property_mixins";
import { SpatialUnits } from "../../core/enums";
import { build_view } from "../../core/build_views";
import * as p from "../../core/properties";
import { atan2 } from "../../core/util/math";
export class ArrowView extends AnnotationView {
    initialize() {
        super.initialize();
        this.set_data(this.model.source);
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        const { start, end } = this.model;
        const { parent } = this;
        if (start != null)
            this.start = await build_view(start, { parent });
        if (end != null)
            this.end = await build_view(end, { parent });
    }
    remove() {
        this.start?.remove();
        this.end?.remove();
        super.remove();
    }
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.change, () => this.set_data(this.model.source));
        this.connect(this.model.source.streaming, () => this.set_data(this.model.source));
        this.connect(this.model.source.patching, () => this.set_data(this.model.source));
        this.connect(this.model.source.change, () => this.set_data(this.model.source));
    }
    set_data(source) {
        super.set_data(source);
        this.plot_view.request_render();
    }
    _map_data() {
        const { frame } = this.plot_view;
        let sx_start, sy_start;
        if (this.model.start_units == 'data') {
            sx_start = this.coordinates.x_scale.v_compute(this._x_start);
            sy_start = this.coordinates.y_scale.v_compute(this._y_start);
        }
        else {
            sx_start = frame.xview.v_compute(this._x_start);
            sy_start = frame.yview.v_compute(this._y_start);
        }
        let sx_end, sy_end;
        if (this.model.end_units == 'data') {
            sx_end = this.coordinates.x_scale.v_compute(this._x_end);
            sy_end = this.coordinates.y_scale.v_compute(this._y_end);
        }
        else {
            sx_end = frame.xview.v_compute(this._x_end);
            sy_end = frame.yview.v_compute(this._y_end);
        }
        return [[sx_start, sy_start], [sx_end, sy_end]];
    }
    _render() {
        const { ctx } = this.layer;
        ctx.save();
        // Order in this function is important. First we draw all the arrow heads.
        const [start, end] = this._map_data();
        if (this.end != null)
            this._arrow_head(ctx, "render", this.end, start, end);
        if (this.start != null)
            this._arrow_head(ctx, "render", this.start, end, start);
        // Next we call .clip on all the arrow heads, inside an initial canvas sized
        // rect, to create an "inverted" clip region for the arrow heads
        ctx.beginPath();
        const { x, y, width, height } = this.plot_view.frame.bbox;
        ctx.rect(x, y, width, height);
        if (this.end != null)
            this._arrow_head(ctx, "clip", this.end, start, end);
        if (this.start != null)
            this._arrow_head(ctx, "clip", this.start, end, start);
        ctx.closePath();
        ctx.clip();
        // Finally we draw the arrow body, with the clipping regions set up. This prevents
        // "fat" arrows from overlapping the arrow head in a bad way.
        this._arrow_body(ctx, start, end);
        ctx.restore();
    }
    _arrow_head(ctx, action, head, start, end) {
        for (let i = 0, _end = this._x_start.length; i < _end; i++) {
            // arrow head runs orthogonal to arrow body
            const angle = Math.PI / 2 + atan2([start[0][i], start[1][i]], [end[0][i], end[1][i]]);
            ctx.save();
            ctx.translate(end[0][i], end[1][i]);
            ctx.rotate(angle);
            if (action == "render")
                head.render(ctx, i);
            else if (action == "clip")
                head.clip(ctx, i);
            ctx.restore();
        }
    }
    _arrow_body(ctx, start, end) {
        if (!this.visuals.line.doit)
            return;
        for (let i = 0, n = this._x_start.length; i < n; i++) {
            this.visuals.line.set_vectorize(ctx, i);
            ctx.beginPath();
            ctx.moveTo(start[0][i], start[1][i]);
            ctx.lineTo(end[0][i], end[1][i]);
            ctx.stroke();
        }
    }
}
ArrowView.__name__ = "ArrowView";
export class Arrow extends Annotation {
    constructor(attrs) {
        super(attrs);
    }
    static init_Arrow() {
        this.prototype.default_view = ArrowView;
        this.mixins(LineVector);
        this.define(({ Ref, Nullable }) => ({
            x_start: [p.XCoordinateSpec],
            y_start: [p.YCoordinateSpec],
            start_units: [SpatialUnits, "data"],
            start: [Nullable(Ref(ArrowHead)), null],
            x_end: [p.XCoordinateSpec],
            y_end: [p.YCoordinateSpec],
            end_units: [SpatialUnits, "data"],
            end: [Nullable(Ref(ArrowHead)), () => new OpenHead()],
            source: [Ref(ColumnarDataSource), () => new ColumnDataSource()],
        }));
    }
}
Arrow.__name__ = "Arrow";
Arrow.init_Arrow();
//# sourceMappingURL=arrow.js.map