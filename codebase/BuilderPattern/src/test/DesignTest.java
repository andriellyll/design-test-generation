package test;

import static org.junit.Assert.*;
import org.junit.Test;

import org.junit.Before;
import org.junit.Ignore;

import java.util.Set;

import org.designwizard.api.DesignWizard;
import org.designwizard.design.ClassNode;
import org.designwizard.design.MethodNode;
import org.designwizard.design.FieldNode;
import org.designwizard.design.PackageNode;

public class DesignTest {
    @Test
    public void testProductConstructorNotUsedDirectly() throws Exception {
        // Always instantiate DesignWizard exactly like this
        DesignWizard dw = new DesignWizard("bin");
        ClassNode productClass = dw.getClass("com.cnblog.clarck.Product");
        ClassNode builderClass = dw.getClass("com.cnblog.clarck.Builder");
        ClassNode directorClass = dw.getClass("com.cnblog.clarck.Director");

        Set<ClassNode> callerClasses = productClass.getCallerClasses();

        assertFalse(callerClasses.contains(productClass));
        assertTrue(callerClasses.contains(builderClass));
        assertTrue(callerClasses.contains(directorClass));
    }

}
