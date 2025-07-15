package com.cnblog.clarck;

import java.util.ArrayList;
import java.util.List;

/**
 * 
 * 
 * @author clarck
 * 
 */
public class Product {
	private List<String> parts = new ArrayList<String>();

	public void add(String part) {
		parts.add(part);
	}

	public void show() {
		System.out.println("");
		for (String part : parts) {
			System.out.println(part);
		}
	}
}
