import { uint32 } from "../types";
export declare function is_color(value: string): boolean;
export declare function rgb2hex(r: number, g: number, b: number): string;
export declare function color2hex(color: string): string;
export declare type RGBAf = [number, number, number, number];
export declare function encode_rgba([r, g, b, a]: RGBAf): uint32;
export declare function decode_rgba(rgba: uint32): RGBAf;
export declare function color2rgba(color: string | null, alpha?: number): RGBAf;
export declare function valid_rgb(value: string): boolean;
//# sourceMappingURL=color.d.ts.map