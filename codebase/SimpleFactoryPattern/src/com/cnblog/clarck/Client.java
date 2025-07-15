package com.cnblog.clarck;

/**
 * 
 * 
 * @author clarck
 * 
 */
public class Client {
	public static void main(String[] args) {
		Product product = ProductFactory.createProduct(ProductType.PRODUCTA);
		String productA = product.createRealProduct();
		System.out.println(productA);

		product = ProductFactory.createProduct(ProductType.PRODUCTA);
		String productB = product.createRealProduct();
		System.out.println(productB);
	}
}
